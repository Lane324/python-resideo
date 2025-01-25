import inspect


class User:
    """
    Contains data about a user.
    """

    userID: int
    username: str
    firstname: str
    lastname: str
    created: int
    deleted: int
    activated: bool
    connectedHomeAccountExists: bool
    locationRoleMapping: list[dict[str, int | str]]
    isOptOut: bool
    isCurrentUser: bool

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if key not in inspect.get_annotations(type(self)):
                raise AttributeError
            setattr(self, key, value)
