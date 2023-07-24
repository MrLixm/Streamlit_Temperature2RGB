import enum


class NamedFunction:
    """
    Override the ``__str__`` magic method of a function so it works with str(function).
    """

    def __init__(self, initial_function, name: str):
        self._initial_function = initial_function
        self._name: str = name

    def __call__(self, *args, **kwargs):
        return self._initial_function(*args, **kwargs)

    def __str__(self):
        return self._name


def widgetify(func):
    """
    Decorator to allow a function to be used a streamlit widget callback AND key.

    >>> import streamlit
    >>>
    >>> def foo(key):
    >>>     print(key)
    >>>
    >>> streamlit.slider(
    >>>     # ...,
    >>>     key=str(foo),
    >>>     on_change=foo,
    >>> )
    """
    _key = func.__name__

    def inner(*args, **kwargs):
        return func(key=_key)

    return NamedFunction(inner, _key)


class UifiedEnum(enum.Enum):
    """
    Each enum member must have a tuple for value with the expected form::

        tuple["ui label", "corresponding value for core"]
    """

    def as_label(self):
        return self.value[0]

    def as_core(self):
        return self.value[1]

    @classmethod
    def from_label(cls, label):
        for item in cls:
            if item.value[0] == label:
                return item
        return None

    @classmethod
    def labels(cls):
        return [item.as_label() for item in cls]
