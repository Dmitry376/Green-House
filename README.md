# Название проекта
Название проекта: «Автоматизированная система удаленного управления теплицей»

# Описание проекта
Проект представляет собой веб-приложение с интерфейсом для управления теплицей. Приложение получает данные о влажности, температуре и влажности почвы в теплице посредством API. Также приложение позволяет отправлять запросы на открытие форточки в теплице, включение полива для каждой из 6 бороздок и включение общего увлажнения.

# Инструкция по запуску
1. Скачайте репозиторий на свой компьютер `git clone https://github.com/Dmitry376/Green-House.git`.
2. Установите все необходимые зависимости, используя команду `pip install -r requirements.txt.`
3. Запустите скрипт для получения новых данных, используя команду `python get_data.py`.
4. Запустите веб-интерфейс `дважды кликните на файл start.bat`.
5. Откройте веб-браузер и перейдите по адресу `http://localhost:8501`, чтобы открыть приложение.

# Остановка получения данных
Для остановки получения данных, закройте консоль Python.

# Используемые технологии
Проект написан на языке Python и использует следующие библиотеки:

- sqlite3 - для работы с базой данных;
- requests - для работы с API;
- json - для работы с json файлами;
- datetime - для получения времени получения / отправки данных;
- pandas - для более удобной обработки данных из базы данных;
- streamlit - для веб-интерфейса.

# Проект создан командой разработчиков:
- 
- 
- 
- 
- 

# Лицензия
Проект распространяется под лицензией MIT. Подробную информацию можно найти в файле `LICENSE.md`.
