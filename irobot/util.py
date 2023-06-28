"""
iRobot packet definitions.

Copyright (c) 2022. 2023 Peter Hagelund

License (MIT):

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


from typing import IO


def hex_dump(data: bytes, io: IO) -> None:
    """Emits the contents of the specified `data` to the specified `io` as hex.

    :param data: the data bytes to emit.
    :param io: the IO instance to write to.
    """
    offset = 0
    while offset < len(data):
        io.write(f"{offset:08x}  ")
        for index in range(16):
            if offset + index < len(data):
                io.write(f"{data[offset + index]:02x} ")
            else:
                io.write("   ")
            if index == 7 or index == 15:
                io.write(" ")
        io.write("|")
        for index in range(16):
            if offset + index < len(data):
                c = data[offset + index]
                if c < 32 or c > 126:
                    io.write(".")
                else:
                    io.write(f"{c:c}")
        io.write("|\n")
        offset += 16
