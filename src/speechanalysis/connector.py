import ctypes


LIB_PATH = "src/connection/conn2khr.so"
lib = ctypes.CDLL(LIB_PATH)


def connect_to_khr() -> int:
    """Connect to KHR-3HV

    Returns:
        int: 0 if success, -1 if fail
    """
    return lib.init()


def disconnect_from_khr() -> None:
    """Disconnect from KHR-3HV"""
    lib.deinit()


def init_command(speed: int=50) -> int:
    """Initialize command structure

    Args:
        speed (int, optional): Speed of servo. Defaults to 50.

    Returns:
        int: 0 if success, -1 if fail
    """
    return lib.init_command(speed)


def add_command(ics: int, pos: int, speed: int=50) -> int:
    """Add command to command structure

    Args:
        ics (int): servo id
        pos (int): position of servo
        speed (int, optional): speed of servo. Defaults to 50.

    Returns:
        int: 0 if success, -1 if fail

    Note: Should not set other speed because the kind of command is const.
    """
    return lib.add_command(ics, speed, pos)


def send_commands() -> int:
    """Send command to KHR-3HV

    Returns:
        int: bytes received
    """
    return lib.send_command()


if __name__ == "__main__":
    """Test connection"""
    print ("\n##### Test connection #####")
    connect_to_khr()
    init_command()
    add_command(0, 100)
    add_command(1, 200)
    send_commands()
    disconnect_from_khr()