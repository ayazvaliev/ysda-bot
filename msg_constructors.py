from msg_templates import *
from config import CAPTION_CAP


def construct_message(urls: list[tuple[str, str]],
                      name: str,
                      desc: str,
                      rating: str,
                      votes: str,
                      year: str):
    if name != "":
        if year != "":
            res = title_scheme % (name, year)
        else:
            res = title_scheme % name
    else:
        res = ""

    if rating != "":
        if votes != "":
            res += rating_scheme % (rating, votes)
        else:
            res += rating_scheme_without_votes % rating

    formatted_urls = ""
    for url, host_name in urls:
        formatted_urls += url_scheme % (url, host_name)

    if len(res) + len(desc) + len(formatted_urls) + 2> CAPTION_CAP:
        desc = desc[:CAPTION_CAP - len(res) - len(formatted_urls) - 5] + '...'
    res += desc + '\n\n'
    res += formatted_urls
    return res


def construct_history_message(history: list[tuple[str, str]]):
    if len(history) == 0:
        return empty_history_msg
    msg = history_title_scheme
    for i, entry in enumerate(history, start=1):
        query, film = entry
        msg += history_scheme % (i, query, film)
    return msg


def construct_stat_message(stats: list[tuple[str, int]]):
    if len(stats) == 0:
        return empty_history_msg
    msg = stats_title_sheme
    for i, stat in enumerate(stats, start=1):
        film, q = stat
        msg += stat_scheme % (i, film, q)
    return msg
