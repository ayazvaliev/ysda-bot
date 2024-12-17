import os
from yarl import URL
from aiohttp import ClientSession
from exceptions import MovieAPIError, MovieNotFound


SEARCH_API = os.getenv("SEARCH_API")
SEARCH_ID = os.getenv("SEARCH_ID")
KINOPOISK_API = os.getenv("KINOPOISK_API")
SEARCH_API_URL = 'https://www.googleapis.com/customsearch/v1'
KINOPOISK_API_URL = 'https://api.kinopoisk.dev/v1.4/movie/'
HOSTS = ['https://gg.vtop.to', 'https://k3.kpfr.fun']


async def get_kinopoisk_url(query: str) -> list[URL]:
    params = {'q': f"site:www.kinopoisk.ru {query}",
              'key': SEARCH_API,
              'cx': SEARCH_ID,
              'num': 5}
    async with ClientSession() as session:
        async with session.get(SEARCH_API_URL, params=params) as resp:
            if resp.status != 200:
                raise MovieAPIError
            resp_json = await resp.json()
    if 'items' not in resp_json:
        raise MovieNotFound
    return [URL(item['link']) for item in resp_json['items']]


def parse_kinopoisk_url(url: URL) -> str | None:
    decomposed = url.path[1:].split('/')
    if decomposed[0] != 'film' and decomposed[0] != 'series':
        return None
    return decomposed[1]


async def get_kinopoisk_info(query: str) -> tuple[str, ...]:
    kinopoisk_urls = await get_kinopoisk_url(query)
    for kinopoisk_url in kinopoisk_urls:
        if (kp_id := parse_kinopoisk_url(kinopoisk_url)) is not None:
            return (kp_id,) + tuple(host + kinopoisk_url.path for host in HOSTS)
    raise MovieNotFound


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


async def get_film_info(kinopoisk_id: str) -> tuple[str, ...]:
    try:
        assert KINOPOISK_API is not None
        async with ClientSession(headers={'X-API-KEY': KINOPOISK_API, 'accept': 'application/json'}) as session:
            async with session.get(KINOPOISK_API_URL + kinopoisk_id) as resp:
                assert resp.status == 200
                resp_json = await resp.json()
        getters = [get_name_from_json, get_desc_from_json, get_rating_from_json,
                   get_votes_from_json, get_poster_from_json, get_year_from_json]

        return tuple(getter(resp_json) for getter in getters)
    except Exception:
        raise MovieAPIError
