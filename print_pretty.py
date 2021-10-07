def print_pretty(item) -> str:
    p = []
    for a in item:
        if a == 0:
            p.append('\u2191')
        elif a == 1:
            p.append('\u2193')
        elif a == 2:
            p.append('\u2190')
        elif a == 3:
            p.append('\u2192')
    return p
