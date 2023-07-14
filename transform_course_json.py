def remove_hidden_items(course_json):
    def remove_hidden_items_rec(item):
        if not item["available"]:
            return None

        pruned_children = []
        for child in item["children"]:
            pruned_child = remove_hidden_items_rec(child)
            if pruned_child is not None:
                pruned_children.append(pruned_child)

        return {
            **item,
            "children": pruned_children,
        }

    pruned_toc = []
    for toc_item in course_json["toc"]:
        if not toc_item["enabled"]:
            continue

        pruned_children = []
        for toc_subitem in toc_item["children"]:
            pruned_child = remove_hidden_items_rec(toc_subitem)
            if pruned_child is not None:
                pruned_children.append(pruned_child)

        pruned_toc.append(
            {
                **toc_item,
                "children": pruned_children,
            }
        )

    return {
        **course_json,
        "toc": pruned_toc,
    }


def remove_empty_items(course_json):
    def remove_empty_items_rec(item):
        if not item["title"] and not item["summary"] and not item["body"]:
            return None

        pruned_children = []
        for child in item["children"]:
            pruned_child = remove_empty_items_rec(child)
            if pruned_child is not None:
                pruned_children.append(pruned_child)

        return {
            **item,
            "children": pruned_children,
        }

    pruned_toc = []
    for toc_item in course_json["toc"]:
        pruned_children = []
        for toc_subitem in toc_item["children"]:
            pruned_child = remove_empty_items_rec(toc_subitem)
            if pruned_child is not None:
                pruned_children.append(pruned_child)

        if pruned_children:
            pruned_toc.append(
                {
                    **toc_item,
                    "children": pruned_children,
                }
            )

    return {**course_json, "toc": pruned_toc}


def replace_macros(course_json):
    replacements = {
        "\n <p>Hello @X@user.full_name@X@, we are pleased to welcome you to @X@course.course_name@X@.</p>": "",
        "@X@course.course_name@X@": course_json["course_name"],
    }

    def replace_macros_rec(item):
        updated_body = item["body"]
        for macro, replacement in replacements.items():
            updated_body = updated_body.replace(macro, replacement)

        updated_children = []
        for child in item["children"]:
            updated_children.append(replace_macros_rec(child))

        return {
            **item,
            "body": updated_body,
            "children": updated_children,
        }

    updated_toc = []
    for toc_item in course_json["toc"]:
        updated_children = []
        for toc_subitem in toc_item["children"]:
            updated_children.append(replace_macros_rec(toc_subitem))
        updated_toc.append(
            {
                **toc_item,
                "children": updated_children,
            }
        )
    return {
        **course_json,
        "toc": updated_toc,
    }


def remove_internal_course_info(course_json):
    updated_toc = []
    for toc_item in course_json["toc"]:
        if toc_item["title"] == "Course Information":
            pruned_children = []
            for child in toc_item["children"]:
                if (
                    not child["description"] == "Course Summary"
                    and not child["title"] == "Timetable"
                    and not child["title"]
                    == "Informatics Teaching Organisation: Information for Students"
                ):
                    pruned_children.append(child)
            updated_toc.append(
                {
                    **toc_item,
                    "children": pruned_children,
                }
            )
        else:
            updated_toc.append(toc_item)
    return {
        **course_json,
        "toc": updated_toc,
    }


def merge_welcome_and_course_info(course_json):
    updated_toc = []
    overview = []
    for toc_item in course_json["toc"]:
        if toc_item["title"] == "Welcome" or toc_item["title"] == "Course Information":
            for child in toc_item["children"]:
                overview_item = f"<h3>{child['title']}</h3>"
                if child["description"]:
                    overview_item += child["description"]
                if child["body"]:
                    overview_item += child["body"]
                overview.append(overview_item)
        else:
            updated_toc.append(toc_item)

    return {
        **course_json,
        "overview": "<br>".join(overview),
        "toc": updated_toc,
    }


def flatten_leaf_children(course_json):
    def get_tree_depth(item, depthSoFar):
        if not item["children"]:
            return depthSoFar
        depthCandidates = []
        for child in item["children"]:
            depthCandidates.append(get_tree_depth(child, depthSoFar + 1))
        return max(depthCandidates)

    def flatten_leaf_children_rec(item):
        depth = get_tree_depth(item, 0)
        if depth < 1:
            return item
        if depth == 1:
            flattened_body = []
            if item["body"]:
                flattened_body.append(item["body"])

            for child in item["children"]:
                flattened_child = f"<h3>{child['title']}</h3>"
                if child["description"]:
                    flattened_child += child["description"]
                if child["body"]:
                    flattened_child += child["body"]
                flattened_body.append(flattened_child)
            return {**item, "body": "<br>".join(flattened_body), "children": []}
        if depth > 1:
            flattened_children = []
            for child in item["children"]:
                flattened_children.append(flatten_leaf_children_rec(child))
            return {**item, "children": flattened_children}

    flattened_toc = []
    for toc_item in course_json["toc"]:
        flattened_children = []
        for toc_subitem in toc_item["children"]:
            flattened_children.append(flatten_leaf_children_rec(toc_subitem))
        flattened_toc.append(
            {
                **toc_item,
                "children": flattened_children,
            }
        )

    return {
        **course_json,
        "toc": flattened_toc,
    }


def apply_transformations(course_json):
    for t in [
        remove_hidden_items,
        remove_empty_items,
        replace_macros,
        remove_internal_course_info,
        merge_welcome_and_course_info,
        flatten_leaf_children,
    ]:
        course_json = t(course_json)

    return course_json
