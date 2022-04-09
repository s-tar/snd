def merge(source, feed):
    for key, value in feed.items():
        if isinstance(value, dict) and key in source:
            merge(source[key], value)
        else:
            source[key] = value

    return source


