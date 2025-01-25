class Config:
    """
    Contains data about a configuration
    """

    faceRecognition: dict[str, bool | int | list[dict[str, list[str, str]] | list[str]]]

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if key not in self.__annotations__:
                raise AttributeError
            setattr(self, key, value)
