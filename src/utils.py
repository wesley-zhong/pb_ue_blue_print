def parser_body_class_by_comment(comment,tag):
    if not comment:
        return None
    key_value_pairs = comment.split(",")
    if len(key_value_pairs) == 0:
        return None
    for pair in key_value_pairs:
        pair = pair.strip()
        if pair == "":
            continue
        print("=============", pair)
        key_value = pair.split("=")
        if len(key_value) != 2:
            continue
        if key_value[0] == tag:
            return key_value[1]
    return None
