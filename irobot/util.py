from typing import IO


def hex_dump(data: bytes, io: IO) -> None:
    """Emits the contents of the specified `data` to the specified `io` as hex.

    Arguments:
    data: the data bytes to emit
    io: the IO instance to write to
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
