from itertools import zip_longest


def merge(source, feed):
    for key, value in feed.items():
        if isinstance(value, dict) and key in source:
            merge(source[key], value)
        elif isinstance(value, list):
            if key not in source:
                source[key] = [v for v in value if v]
                continue

            for i, (s, v) in enumerate(zip_longest(source[key], value)):
                if v is None:
                    continue
                if len(source[key]) > i:
                    source[key][i] = v
                else:
                    source[key].append(v)

            source[key] = [
                value
                for value in source[key]
                if value not in {None, ""}
            ]
        else:
            source[key] = value

    return source


