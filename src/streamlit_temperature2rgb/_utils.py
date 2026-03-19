import enum
from typing import Sequence
from typing import Union


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


def python_to_markdown_table(
    python_table: Union[tuple[Union[tuple, list]], list[Union[tuple, list]]],
    headers: list[str],
) -> str:
    """
    Convert a table stored as a python object (list of list usually), to a markdown formatted table.
    """
    table_colum_len = [
        max(column)
        for column in [[len(item) for item in column] for column in zip(*python_table)]
    ]

    markdown_table = ""

    for column_index, column_length in enumerate(table_colum_len):
        markdown_table += "|" + headers[column_index].ljust(column_length, " ")

    markdown_table += "|\n"

    for column_length in table_colum_len:
        markdown_table += "|" + "-" * column_length

    markdown_table += "|\n"

    for row in python_table:
        for column_index, column_length in enumerate(table_colum_len):
            markdown_table += "|" + row[column_index].ljust(column_length, " ")

        markdown_table += "|\n"

    return markdown_table
