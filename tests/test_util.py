"""
Tests for util.
"""


from inspect import cleandoc
from io import StringIO

from irobot.util import hex_dump

dump = """
    00000000  21 22 23 24 25 26 27 28  29 2a 2b 2c 2d 2e 2f 30  |!"#$%&'()*+,-./0|
    00000010  31 32 33 34 35 36 37 0a  39 3a 3b 3c 3d 3e 3f 40  |1234567.9:;<=>?@|
    00000020  41 42 43 44 45 46 47 48  49 4a                    |ABCDEFGHIJ|
    """


def test_hex_dump():
    """Tests that `hex_dump` emits the correct information."""
    io = StringIO()
    a = [0] * 42
    for i in range(len(a)):
        a[i] = 33 + i
    a[23] = 10
    data = bytes(a)
    hex_dump(data, io)
    value = io.getvalue()
    assert value.rstrip() == cleandoc(dump)
