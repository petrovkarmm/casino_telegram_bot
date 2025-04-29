def parse_bet_slug(slug: str) -> int:
    parts = slug.split('_')
    sign = 1 if parts[1] == 'plus' else -1
    value = int(parts[2])
    return sign * value
