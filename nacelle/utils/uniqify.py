def uniqify(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if x not in seen and not seen_add(x)]


def uniqify_keys(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if x.id() not in seen and not seen_add(x.id())]


def uniqify_models(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if x.key.id() not in seen and not seen_add(x.key.id())]
