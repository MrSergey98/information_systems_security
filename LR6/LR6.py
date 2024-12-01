import socket
from winreg import *


def can_access_to_program():
    IP = '192.168.1.31'
    CPU = '12th Gen Intel(R) Core(TM) i5-12400F'
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    aReg = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
    aKey = OpenKey(aReg, r"HARDWARE\DESCRIPTION\System\CentralProcessor\0")
    cpu = QueryValueEx(aKey, 'ProcessorNameString')[0]

    return ip == IP and CPU == cpu


def private_func():
    print("You have access to program!")


def have_no_access():
    print('You have no access to program!')


if __name__ == '__main__':
    if can_access_to_program():
        private_func()
    else:
        have_no_access()
    input()