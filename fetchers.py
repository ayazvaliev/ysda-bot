import os
from yarl import URL
from aiohttp import ClientSession
from exceptions import MovieAPIError, MovieNotFound
import logging

SEARCH_API = os.getenv("SEARCH_API")
SEARCH_ID = os.getenv("SEARCH_ID")
KINOPOISK_API = os.getenv("KINOPOISK_API")
SEARCH_API_URL = 'https://www.googleapis.com/customsearch/v1'
KINOPOISK_API_SEARCH_URL = 'https://api.kinopoisk.dev/v1.4/movie/search'
BACKUP_HOSTS = ['gidonline', 'lordfilm', 'hdreska', 'hdrezka',
                'kinogo', 'rezka', 'rutube', 'ok.ru']
ANIME_HOSTS = ['jut.su', 'animego', 'yummyani']
HOST_TO_NAME = {
    'gidonline': 'ГидОнлайн',
    'lordfilm': 'LordFilm',
    'hdreska': 'HDReska',
    'hdrezka': 'HDRezka',
    'kinogo': 'КиноГо',
    'rezka': 'Rezka',
    'rutube': 'Rutube',
    'ok.ru': 'Одноклассники',
    'jut.su': 'JutSu',
    'animego': 'AnimeGo',
    'yummyani': 'YummyAnime'
}
TYPE_TO_QUERY = {
    'movie': 'фильм',
    'anime': 'аниме',
    'series': 'сериал',
    '': ''
}
HOSTS = [('https://gg.vtop.to', 'GGKinopoisk'), ('https://k3.kpfr.fun', 'FreeKinopoisk')]


async def google_search(query: str, site: str | None, num=1) -> list[URL]:
    if site is not None:
        query = f"site:{site} " + query
    logging.info(query)
    params = {
        'q': query,
        'key': SEARCH_API,
        'cx': SEARCH_ID,
        'num': num
    }
    async with ClientSession() as session:
        async with session.get(SEARCH_API_URL, params=params) as resp:
            if resp.status != 200:
                raise MovieAPIError
            resp_json = await resp.json()
    if 'items' not in resp_json:
        return list()
    return [URL(item['link']) for item in resp_json['items']]


def parse_kinopoisk_url(url: URL) -> None | tuple[str, str]:
    decomposed = url.path[1:].split('/')
    if decomposed[0] != 'film' and decomposed[0] != 'series':
        return None
    return decomposed[0], decomposed[1]


'''
async def get_kinopoisk_info(query: str) -> tuple[str, str]:
    kinopoisk_urls = await google_search(query, site='www.kinopoisk.ru', num=5)
    for kinopoisk_url in kinopoisk_urls:
        if (res := parse_kinopoisk_url(kinopoisk_url)) is not None:
            type_, kp_id = res
            return type_, kp_id
    raise MovieNotFound
'''


async def get_pirate_urls(kp_id: str, name: str, type_: str, is_series: str) -> list[tuple[str, str]]:
    is_series_bool = True if is_series == 'True' else False
    if type_ not in TYPE_TO_QUERY:
        type_ = ''
    query = f'{name} {TYPE_TO_QUERY[type_]} смотреть онлайн бесплатно'
    HOSTS_TO_SEARCH = ANIME_HOSTS if type_ == 'anime' else BACKUP_HOSTS
    search_urls: list[URL] = await google_search(query, site=None, num=10)
    valid_urls = []

    for host in HOSTS:
        host_name, title = host
        url = host_name + '/' + ('film' if not is_series_bool else 'series') + '/' + kp_id
        valid_urls.append((url, title))

    for url in search_urls:
        if url.host is None:
            continue
        for pirate_host in HOSTS_TO_SEARCH:
            if url.host.find(pirate_host) != -1:
                valid_urls.append((str(url), HOST_TO_NAME[pirate_host]))
                break
    return valid_urls


def get_kp_id_from_json(resp_json) -> str:
    kp_id = ''
    if 'id' in resp_json:
        kp_id = str(resp_json['id'])
    return kp_id


def get_type_from_json(resp_json) -> str:
    type_ = ''
    if 'type' in resp_json:
        type_ = resp_json['type']
    return type_


def get_poster_from_json(resp_json) -> str:
    poster = ''
    if 'poster' in resp_json:
        poster = resp_json['poster']['url']
    return poster


def get_rating_from_json(resp_json) -> str:
    rating = ''
    if 'rating' in resp_json:
        rating = str(resp_json['rating']['kp'])
    return rating


def get_votes_from_json(resp_json) -> str:
    votes = ''
    if 'votes' in resp_json:
        votes = str(resp_json['votes']['kp'])
    return votes


def get_name_from_json(resp_json) -> str:
    name = ''
    if 'name' in resp_json:
        name = resp_json['name']
    return name


def get_desc_from_json(resp_json) -> str:
    desc = ''
    if 'description' in resp_json:
        desc = resp_json['description']
    return desc


def get_year_from_json(resp_json) -> str:
    year = ''
    if 'year' in resp_json:
        year = str(resp_json['year'])
    return year


def get_is_series_from_json(resp_json) -> str:
    is_series = 'False'
    if 'isSeries' in resp_json:
        is_series = str(resp_json['isSeries'])
    return is_series

async def get_film_info(query: str) -> tuple[str, ...]:
    try:
        assert KINOPOISK_API is not None
        async with ClientSession(headers={'X-API-KEY': KINOPOISK_API, 'accept': 'application/json'}) as session:
            async with session.get(KINOPOISK_API_SEARCH_URL,
                                   params={'query': query,
                                           'page': 1,
                                           'limit': 1}) as resp:
                logging.info(resp.status)
                assert resp.status == 200
                resp_json = await resp.json()
        if ('docs' not in resp_json) or len(resp_json['docs']) == 0:
            raise MovieNotFound
        movie_json = resp_json['docs'][0]
        getters = [get_kp_id_from_json, get_name_from_json, get_desc_from_json, get_rating_from_json,
                   get_votes_from_json, get_poster_from_json, get_year_from_json, get_type_from_json,
                   get_is_series_from_json]

        return tuple(getter(movie_json) for getter in getters)
    except Exception:
        raise MovieAPIError
