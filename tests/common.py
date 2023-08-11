from collections import OrderedDict
from random import choices
from string import ascii_lowercase, ascii_uppercase, digits


class TestRecord(OrderedDict):
    """
    Provides a very similar Record class to that returned by asyncpg.  A custom implementation
    is needed as it is currently impossible to create asyncpg Record objects from Python code.
    [https://github.com/MagicStack/asyncpg/issues/480]
    """

    def __getitem__(self, key_or_index):
        if isinstance(key_or_index, int):
            return list(self.values())[key_or_index]

        return super().__getitem__(key_or_index)


def random_string(n=16, with_digits=True, with_uppercase=True) -> str:
    base = ascii_lowercase

    if with_uppercase:
        base += ascii_uppercase

    if with_digits:
        base += digits

    return "".join(choices(base, k=n))
