def strip_prefix_from_item(item, prefix):
    if isinstance(item, str):
        return item[len(prefix):] if item.startswith(prefix) else item
    if isinstance(item, list):
        return [strip_prefix_from_item(x, prefix) for x in item]
    return item

def flatten(item):
    out = []
    if isinstance(item, str):
        out.append(item.lower())
    elif isinstance(item, list):
        for x in item:
            out.extend(flatten(x))
    return out
