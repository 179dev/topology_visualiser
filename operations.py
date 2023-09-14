from config import expect_lib

# from pexpect import popen_spawn
import re
import time


def start_ssh(ip: str, login: str, password: str, pxp: expect_lib.spawn | None = None) -> expect_lib.spawn:
    if pxp is None:
        pxp = expect_lib.spawn(f"ssh {login}@{ip}")
    else:
        pxp.expect("$")
        print("На бызовом устройстве")
        print("Подключение дальше по ssh")
        pxp.sendline(f"ssh {login}@{ip}")
    time.sleep(5)
    result = pxp.expect(["password:", "(yes/no)"])
    if result == 1:
        pxp.sendline("yes")
    pxp.sendline(f"{password}")
    pxp.sendline("terminal length 0")
    return pxp


# class DeviceInfo:
#     ip_address: str
#     device_id: str
#     interface: str
#     port_id: str

#     software: str
#     version: str

# def start_telnet(ip: str, port: str):
#     print(f"Подключение к {ip} {port}...")
#     pxp = expect_lib.spawn(f"telnet {ip} {port}")
#     # pxp.expect("Escape")
#     pxp.sendline("\n")
#     result = pxp.expect([".*>", ".*#", expect_lib.TIMEOUT])
#     if result == -1:
#         print("TIMEOUT")
#     else:
#         print(f"Подключен к {ip} {port}")
#     if result == 0:
#         enter_privileged_mode(pxp)
#     pxp.sendline("terminal length 0")
#     pxp.expect([".*>", ".*#"])
#     print("Включен режим полного вывода")
#     return pxp

# def start_telnet(ip: str, port: str):
#     print(f"Подключение к {ip} {port}...")
#     pxp = expect_lib.spawn(f"telnet {ip} {port}")
#     # pxp.expect("Escape")
#     pxp.sendline("\n")
#     result = pxp.expect([".*>", ".*#", expect_lib.TIMEOUT])
#     if result == -1:
#         print("TIMEOUT")
#     else:
#         print(f"Подключен к {ip} {port}")
#     if result == 0:
#         enter_privileged_mode(pxp)
#     pxp.sendline("terminal length 0")
#     pxp.expect([".*>", ".*#"])
#     print("Включен режим полного вывода")
#     return pxp


def enter_privileged_mode(pxp: expect_lib.spawn):
    print("Вход в привелигированный режим...")
    pxp.sendline("enable")
    result = pxp.expect([".*#", "Password"])
    match result:
        case 0:
            pass
        case 1:
            pxp.sendline("cisco")
            pxp.expect(".*#")

    print("Accesed")


def get_neig_data(pxp: expect_lib.spawn) -> str:
    print("Получение данныx с устройства...")
    pxp.sendline("terminal length 0")
    pxp.sendline("show cdp neig det")
    pxp.expect("--.+$", re.DOTALL)
    data = pxp.after
    # pxp.expect([".*>", ".*#"])
    print("Данные полученны")
    return data

def parse_neighbors(output: str) -> dict:
    matches = []
    for block in output.split("-------------------------"):
        match = re.search(
            r"Device ID ?: ?(?P<device_id>\w+)"
            r".+IP address ?: ?(?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"
            r".+Interface ?: ?(?P<interface>\S+)"
            r".+Port ID \(outgoing port\) ?: ?(?P<port_id>\S+)"
            r".+Software \((?P<software>\S+)\)"
            r".+Version (?P<version>.+?)(,\s|$)$",
            block,
            re.DOTALL | re.MULTILINE,
        )
        if match:
            matches.append(match.groupdict())
    return matches

def roam_net(pxp: expect_lib.spawn, entry_ip: str, username: str, password: str, send_connections=False, 
             connections_buffer: list=None, devices_buffer: list=None):
    start_ssh(ip=entry_ip, login=username, password=password, pxp=pxp)
    #enter_privileged_mode(pxp)
    stack = parse_neighbors(get_neig_data(pxp)) 
    visited = [entry_ip]
    print('Анализ сети')
    pxp.sendline('exit')
    while stack:
        device = stack.pop(0)
        if device["id"] in visited:
            continue
        print(f'Подключение к {username}@{device["ip"]}')
        start_ssh(ip=device['ip'], login=username, password=password, pxp=pxp)
        #enter_privileged_mode(pxp)
        print('Подключено. Получение данных о соседях')
        neighs = parse_neighbors(get_neig_data(pxp))
        print('Обнаружено', len(neighs), 'соседей')
        for neigh in neighs:
            if neigh['ip'] not in visited:
                stack.append(neigh)
            elif send_connections:
                name_in = f'{device["ip"]} - {device["device_id"]}'
                name_out = f'{neigh["ip"]} - {neigh["device_id"]}'
                if connections_buffer is not None:
                    connections_buffer.append(
                        ((device["ip"], device["device_id"], neigh["port_id"]), 
                         (neigh["ip"], neigh["device_id"], neigh["interface"]))
                    )
                yield ((name_in, neigh["port_id"]), (name_out, neigh["interface"]))
        visited.append(device['ip'])
        if not send_connections:
            yield device
        if devices_buffer is not None:
            devices_buffer.append(device)
        print('Возврат к внешней машине')
        pxp.sendline('exit')