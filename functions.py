import dialog
import time
def select_snapshot():
    answer = input (dialog.init)
    match answer:
        case "1":
            print ("Инициализировать сеть")
        case "2":
            print ("Использовать последний снапшот")
        case "3":
            print ("Выбрать снапшот")
    return snap

def create_snapshot():
    print ("Создание снапшота")
    filename = f"snapshots/net_snapshot{time}.csv"
    with open(filename, "w") as f:
        f.write(dialog.csv_columns)

    return filename

def add_data_to_snapshot(snapshot_name, data):
    print (f"Редактирование {snapshot_name}")
    with open(snapshot_name, "a+") as f:
        text = f.read()
        for device in data:
            if device["device_id"] not in text:
                to_write = (device["device_id"]
                            + "," + device["ip"]
                            + "," + device["software"]
                            + "," + device["version"]
                )
                f.write(to_write)
