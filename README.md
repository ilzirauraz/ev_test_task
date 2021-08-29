# ev_test_task

В системе работаю 3 компонента: Контроллер(разбито на веб-сервер и периодическую задачу), манипулятор и сенсор.  
Данные с сенсоров хранятся в  Redis ttl=5 сек

Запуск системы:

1. Запустить Redis и Контроллер:  
``` docker-compose up redis controller ```

2. Запустить Манипулятор:  
``` docker-compose up manipulator ```

3. Запустить 8 Сенсоров:  
``` docker-compose up --scale sensor=8 sensor ```

4. Запустить периодические задачи:  
``` docker-compose up controller_periodic_task ```


Примечание  
Проверялось на MacOS и Ubuntu, при использовании стандартной библиотеки socket контейнеры запускались долго, нужно будет подождать.
Либо быстрее будет запустить manipulator и periodic_task локально.

Запуск локально:

1. Создать и активировать виртуальное окружение

2. Установить зависимости:  
``` pip3 install -r requirements.txt ```

3. Запустить Redis и Контроллер:  
``` docker-compose up redis controller ```

2. Запустить Манипулятор:  
``` python manipulator/manipulator.py ```

3. Запустить 8 Сенсоров:  
``` docker-compose up --scale sensor=8 sensor ```

4. Запустить периодические задачи:  
``` python controller/periodic_task.py ```
