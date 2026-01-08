

# ─────────────────────────
# Text formatting
# ─────────────────────────

def cut_line(line: str, max_len: int = 12, fill: str = "."):
    """
    Обрезает строку до слова которое вмещается в заданную максимальную длину,
    и добавляет заполнитель
    """
    if len(line) <= max_len:
        return line

    while len(line) > max_len:
        if (space_idx := line.rfind(" ")) != -1:
            line = line[:space_idx]
        else:
            return line[:max_len - 2] + fill * 2
    return line + fill * (max_len - len(line))


def bold(text: str) -> str:
    return f"<b>{text}</b>"


def underlined(text: str) -> str:
    return f"<u>{text}</u>"


def monospace(text: str) -> str:
    return f"<code>{text}</code>"


# ─────────────────────────
# Currency
# ─────────────────────────

def currency_sign(currency: str) -> str:
    return {
        "EUR": "€",
        "RUB": "₽",
        "USD": "$",
    }.get(currency, "¤")
