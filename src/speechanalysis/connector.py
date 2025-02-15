import ctypes

LIB_PATH = 'src/connection/conn2khr.so'
lib = ctypes.CDLL(LIB_PATH)


def connect_to_khr() -> int:
    return lib.init()


def disconnect_from_khr() -> int:
    return lib.deinit()


def init_command(speed: int=50) -> int:
    return lib.init_command(speed)


def add_command(ics: int, pos: int, speed: int=50) -> int:
    return lib.add_command(ics, speed, pos)


def send_commands() -> int:
    return lib.send_command()

if __name__ == '__main__':
    print("Conneting test")
    connect_to_khr()
    init_command()
    add_command(0, 100)
    add_command(1, 200)
    send_commands()
    disconnect_from_khr()