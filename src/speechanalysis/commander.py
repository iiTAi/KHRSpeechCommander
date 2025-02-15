import numpy as np

from .connector import (
    connect_to_khr,
    disconnect_from_khr,
    init_command,
    add_command,
    send_commands,
)
from .command_dict import (
    ics_dict,
    option_dict,
    direction_dict,
)


_ics_limit = {
    1: {"min": 3750, "max": 11250},
    2: {"min": 5000, "max": 10000},
    3: {"min": 5000, "max": 12500},
    4: {"min": 2500, "max": 10000},
    5: {"min": 6875, "max": 12500},
    6: {"min": 2500, "max": 8125},
    7: {"min": 3750, "max": 11250},
    8: {"min": 3750, "max": 11250},
    9: {"min": 4375, "max": 8125},
    10: {"min": 6875, "max": 10625},
    11: {"min": 6250, "max": 10000},
    12: {"min": 5000, "max": 8750},
    13: {"min": 6875, "max": 8125},
    14: {"min": 6875, "max": 8125},
    15: {"min": 4375, "max": 10625},
    16: {"min": 4375, "max": 10625},
    17: {"min": 6250, "max": 11875},
    18: {"min": 3125, "max": 8750},
    19: {"min": 5000, "max": 11250},
    20: {"min": 3750, "max": 10000},
    21: {"min": 6875, "max": 10625},
    22: {"min": 4375, "max": 8125},
}


class Commander:
    """Command-sending class for KHR-3HV"""

    def __init__(self, speed: int=50) -> None:
        """Initialize Commander"""
        self.__current_pos = {i: 7500 for i in range(1, len(_ics_limit)+1)}
        self.__command_buffer = {
            "speed": speed,
            "ics_list": [],
            "option": 1,
            "direction": 0,}

    def __del__(self) -> None:
        """Destructor of Commander"""
        self.disconnect()

    def init_connection(self) -> None:
        """Initialize connection to KHR-3HV"""
        connect_to_khr()
        init_command()
        self.reset_position()

    def disconnect(self) -> None:
        """Disconnect from KHR-3HV"""
        self.reset_position()
        self.reset_command_buffer()
        disconnect_from_khr()

    def send_command(self) -> None:
        """Add command to command structure and send it to KHR-3HV

        Command elements are adjusted before sending.
        """
        print("Sending command...")
        for ics in self.__command_buffer["ics_list"]:
            direction = self.__command_buffer["direction"]

            ics = self.__adjust_ics(ics, direction)
            direction = self.__adjust_direction(ics, direction)
            pos = self.__calc_position(ics, direction)

            add_command(
                ics=ics,
                pos=pos,
                speed=self.__command_buffer["speed"],)
            
            print(f"added: isc={ics}, pos={pos}, speed={self.__command_buffer['speed']}")
            self.__current_pos[ics] = pos

        send_commands()
        print("Command sent. (Maybe)")
        # print(f"Current position:\n{self.__current_pos}")

    def reset_position(self) -> None:
        """Reset position of all servos"""
        for ics in self.__current_pos.keys():
            self.__current_pos[ics] = 7500
        for ics in range(1, len(_ics_limit)+1):
            add_command(
                ics=ics,
                pos=7500,
                speed=self.__command_buffer["speed"],)
        send_commands()
        print("Position reset.")
            
    def __adjust_ics(self, ics: int, direction: int) -> int:
        """Adjust ics number according to direction

        Args:
            ics (int): servo id
            direction (int): direction of servo

        Returns:
            int: adjusted ics number
        """
        dir_abs = np.abs(direction)
        match ics:
            case 3|4:
                if dir_abs == 2:
                    ics += 2
            case 7|8:
                if dir_abs == 2:
                    ics += 2
            case 11|12:
                if dir_abs == 1:
                    ics += 4
                elif dir_abs == 2:
                    ics += 2
            case 19|20:
                if dir_abs == 2:
                    ics += 2
        return ics
    
    def __adjust_direction(self, ics: int, direction) -> int:
        """Adjust direction according to ics number

        Args:
            ics (int): servo id
            direction (_type_): direction of servo

        Returns:
            int: adjusted direction
        """
        match ics:
            case 4|6|7|8|10|11|12|14|16|17|19|21:
                direction = -direction

        if direction > 0:
            return 1
        elif direction < 0:
            return -1
        else:
            return 0
        
    def __calc_position(self, ics: int, direction: int) -> int:
        """Calculate position of servo

        Args:
            ics (int): servo id
            direction (int): direction of servo

        Returns:
            int: calculated position
        """
        option = self.__command_buffer["option"]
        pos = self.__current_pos[ics] + int(2500 * option * direction)

        if pos < _ics_limit[ics]["min"]:
            pos = _ics_limit[ics]["min"]
        elif pos > _ics_limit[ics]["max"]:
            pos = _ics_limit[ics]["max"]
        
        return pos
    
    def fetch_current_pos(self) -> dict:
        """Fetch current position of servos"""
        return self.__current_pos
    
    def fetch_command_buffer(self) -> dict:
        """Fetch command buffer"""
        return self.__command_buffer
    
    def fetch_ics_list(self) -> list:
        """Fetch list of ics"""
        return self.__command_buffer["ics_list"]
    
    def fetch_option(self) -> float:
        """Fetch option"""
        return self.__command_buffer["option"]
    
    def fetch_direction(self) -> int:
        """Fetch direction"""
        return self.__command_buffer["direction"]
    
    def set_speed(self, speed: int) -> None:
        """Set speed of servo"""
        self.__command_buffer["speed"] = speed

    def reset_command_buffer(self) -> None:
        """Reset command buffer"""
        self.__command_buffer = {
            "speed": 50,
            "ics_list": [],
            "option": 1,
            "direction": 0,}

    def add_ics(self, ics: int) -> None:
        """Add ics to command buffer"""
        self.__command_buffer["ics_list"].append(ics)

    def set_speed(self, speed: int) -> None:
        """Set speed of servo"""
        self.__command_buffer["speed"] = speed
    
    def set_option(self, option: float) -> None:
        """Set option"""
        self.__command_buffer["option"] = option

    def set_direction(self, direction: int) -> None:
        """Set direction"""
        self.__command_buffer["direction"] = direction


if __name__ == "__main__":
    """Test connection"""
    commander = Commander()
    commander.init_connection()
    commander.add_ics(1)
    commander.add_ics(2)
    commander.set_option(0.5)
    commander.set_direction(1)
    commander.send_command()
    commander.disconnect()