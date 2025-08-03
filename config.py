__all__ = ['SEARCH_API',
           'SEARCH_ID',
           'KINOPOISK_API',
           'SEARCH_API_URL',
           'KINOPOISK_API_SEARCH_URL',
           'BACKUP_HOSTS',
           'ANIME_HOSTS',
           'HOST_TO_NAME',
           'TYPE_TO_QUERY',
           'HOSTS',
           'TIMEOUT']


#Search config
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
TIMEOUT = 5


#sqlite3 local DB
LOCAL_DB = 'db/cinemabot.db'


#message constructor config
CAPTION_CAP = 1024