from topology_visualizer.igraph_topology_visualizer import IgraphTopologyVisualizer as default_visualizer
# from topology_visualizer.graphviz_topology_visualizer import GraphvizTopologyVisualizer as default_vizualizer

import dialog
import os

import functions as fu
import operations as op
from getpass import getpass

def snapshot_dialog():
    while True:
        option = input(dialog.select_snapshot)
        match option:
            case "1":
                return create_new_snapshot()
            case "2":
                return fu.most_recent_snapshot()
            case "3":
                return fu.select_snapshot()

                

def create_new_snapshot():
    print('Создание образа сети...')
    snapshot_id = fu.create_snapshot()

    try:
        userdata = dialog.net_access_user_data()
        outer_ip, outer_login, outer_password = userdata['outer']
        entry_ip, entry_login, entry_password = userdata['entry']
        
        main_pxp = op.start_ssh(outer_ip, outer_login, outer_password)

        connections_buffer = []
        data_iterator = op.roam_net(pxp=main_pxp, entry_ip=entry_ip, 
                                    username=entry_login, password=entry_password, 
                                    send_connections=False,
                                    connections_buffer=connections_buffer)

        fu.add_data_to_snapshot(snapshot_id, data_iterator)
        fu.add_connections_data_to_snapshot(snapshot_id, connections_buffer)
        print(f'Образ сети с {snapshot_id} сохранён')
        return snapshot_id
    except Exception as e:
        fu.delete_snapshot(snapshot_id)
        print('[!] Произошла ошибка при создании образа сети. Битые образы удалены')
        raise e

if __name__ == "__main__":
    while True:
        answer = input(dialog.main)
        match answer:
            case "1":
                create_new_snapshot()
            case "2":
                print ("Построить топологию сети")
                snapshot_id = snapshot_dialog()
                connections = {}
                for key, value in fu.read_connections_snapshot(snapshot_id):
                    connections[key] = value
                    # userdata = dialog.net_access_user_data()
                    # outer_ip, outer_login, outer_password = userdata['outer']
                    # entry_ip, entry_login, entry_password = userdata['entry']

                    # main_pxp = op.start_ssh(outer_ip, outer_login, outer_password)
                    # print('Подключение к первой машине в сети')

                    # graphname = lambda ip, id, port: (f"{id} - {ip}", port)

                    # connections = {graphname(key): graphname(value)
                    #                 for key, value in op.roam_net(
                    #     pxp=main_pxp, entry_ip=entry_ip, username=entry_login, 
                    #     password=entry_password, send_connections=True
                    # )}
                #print(connections)
                for key, value in list(connections.items()):
                    if value in connections:
                        del connections[key]
                #print(connections)
                from topology_visualizer.graphviz_topology_visualizer import GraphvizTopologyVisualizer
                graphname = lambda ip, id, port: (f"{id} - {ip}", port)
                gtv = GraphvizTopologyVisualizer({
                    graphname(key): graphname(value) 
                    for key, value in connections.items()
                })
                gtv.draw(input('Имя файла изображения: '))
                print('Схема топологии сохранена')
            case "3":
                snapshot_id = snapshot_dialog()
                print ("Запрос параметров устройтсва")
                device_ip = fu.select_device(snapshot_id)
                param = fu.select_params(snapshot_id)
                print (fu.get_data(snapshot_id, device_ip, param))
            case "4":
                snapshot_id = snapshot_dialog()
                print ("Выполнить команды в конфигурационном режиме")
            case "5":
                snapshot_id = snapshot_dialog()
                print ("Выполнить команды и записать их вывод")
            case "0":
                print("Выход из программы")
                break
            case _:
                print("Выберите цифру из списка")
