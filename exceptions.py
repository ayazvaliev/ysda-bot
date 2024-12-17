class UndefinedUser(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class MovieNotFound(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class MovieAPIError(Exception):
    def __init__(self, *args):
        super().__init__(*args)
