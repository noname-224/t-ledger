def cut_line(line: str, max_len: int = 20, fill: str = ".."):
    if len(line) <= max_len:
        return line

    cutted = line[:max_len - len(fill)]
    if (space := cutted.rfind(" ")) != -1:
        return cutted[:space] + fill
    return cutted + fill
