def parse_bet_slug(slug: str) -> int:
    parts = slug.split('_')
    sign = 1 if parts[1] == 'plus' else -1
    value = int(parts[2])
    return sign * value


def is_bet_winning(bet_id: str, number: int, color: str) -> bool:
    if bet_id == "bet_black":
        return color == "⚫"
    elif bet_id == "bet_red":
        return color == "🔴"
    elif bet_id == "bet_green":
        return number == 0
    elif bet_id == "bet_even":
        return number != 0 and number % 2 == 0
    elif bet_id == "bet_odd":
        return number % 2 == 1
    elif bet_id == "bet_small":
        return 1 <= number <= 18
    elif bet_id == "bet_big":
        return 19 <= number <= 36
    return False
