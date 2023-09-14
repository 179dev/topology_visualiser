# Что это за проект?
Это совместный проект Spidz, Kaz и Zhur в рамках образовательной программы "Кейс-каникулы в КРОК"

# О чем этот проект?
Рутина системных администраторов состоит из большого количества задач, множество которых можно автоматизировать. Именно в автоматизации таких задач и заключается суть нашего проекта.

# Что может этот проект?
С помощью нашего проекта можно:
- Построить схему топологии сети
- Сохранить данные о сети
# Как запустить проект?
## Установка для Windows
- Установите Python 3.11.x
    - Скачайте [установщик](https://www.python.org/downloads/)
    - Запустите процесс установки
    - __Убедитесь, что Python указан в PATH__
        - В командной строке при вызове `echo %PATH%` в выводе должно быть `..\Python311`, `..\Python311\Scripts`
        - Если их нет, то внесите Python в PATH
            - Откройте `Win+R` `sysdm.cp`
            - Выберите раздел "Дополнительно"
            - Перейдите в `Переменные среды`
            - Нажмите два раза на `Path`
            - Выбрерите `Создать`
            - Введите путь к Python (по умолчанию `C:\Users\<uesrname>\AppData\Local\Python311`)
            - Введите путь к папке Scripts (по умолчанию `C:\Users\<uesrname>\AppData\Local\Python311\Scripts`)
            - Перезапустите консоль
- Установите нужные библиотеки
    - `pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org wexpect pandas cryptography graphviz`
- Установите Graphviz
    - Скачайте и запустите [установщик](https://gitlab.com/api/v4/projects/4207231/packages/generic/graphviz-releases/9.0.0/windows_10_cmake_Release_graphviz-install-9.0.0-win64.exe)
    - Убедитесь, что при установке Graphviz был добавлен в PATH
- Запустите проект
    - Запустите файл `main.py`