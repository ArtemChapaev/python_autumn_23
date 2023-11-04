import json


def parse_json(json_str: str, required_fields: list, keywords: list, keyword_callback):
    if required_fields is None or keywords is None or keyword_callback is None:
        return

    if not isinstance(json_str, str):
        raise TypeError("json_str must be str")
    if not isinstance(required_fields, list):
        raise TypeError("required_fields must be list")
    if not isinstance(keywords, list):
        raise TypeError("keywords must be list")

    json_doc = {}
    try:
        json_doc = json.loads(json_str)
    except json.JSONDecodeError:
        pass

    keywords = [keyword.lower() for keyword in keywords]

    for field, value in json_doc.items():
        if field not in required_fields:
            continue
        # else
        for keyword in value.lower().split():
            if keyword in keywords:
                keyword_callback(field, keyword)
