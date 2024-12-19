title_scheme = "<b>%s (%s)</b>\n\n"
title_scheme_without_year = "<b>%s</b>\n\n"
rating_scheme_without_votes = "Рейтинг на Кинопоиске: <b>%s</b>\n\n"
rating_scheme = "Рейтинг на Кинопоиске: <b>%s</b> (%s)\n\n"
desc_scheme = "%s\n\n"
url_scheme = '<a href="%s">Смотреть на %s</a>\n'
empty_history_msg = "Your history is empty"
stats_title_sheme = "<b>Search Statistics:</b>\n\n"
stat_scheme = "%u. <b>%s</b> <i>%u times</i>\n"
history_title_scheme = "<b>Search History:</b>\n\n"
history_scheme = "%u. <i>Query</i>: %s answered by <b>%s</b>\n"

start_msg = """<b>Bebra Cinemabot</b> - searches films and places to watch them for free from your queries.\
For all information about functionality refer to /help\n\n\n
And remember: <b>Intellectual property is theft</b>"""

help_msg = """/start - Start chat with <b>Bebra Cinemabot</b>
/help - Displays this message
/stats - Displays how many times each film has been found for you
/history - Displays history of queries and found films based on each query\n
In order to enter a query, just send raw message to the bot with title of the film. \
Examples:\n
<code>Venom 2018</code>\n
<code>Остров собак</code>\n\n
<b>ATTENTION</b>: Good accuracy of queries with just the title of the film \
(considering there are multiple films with this title), use extra information \
in cases of mismatch (adding year to the query is usually enough)"""

CAPTION_CAP = 1024

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
