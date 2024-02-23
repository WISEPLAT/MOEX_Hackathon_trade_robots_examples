# Исходные коды API сервиса GO.ALGO.Neuro 
## Сервис создания и проверки торговых и инвестиционных стратегий на базе нейронных сетей [HOW-TO-GUIDE](https://github.com/DaniilVdovin/goalgomoex_master_server/blob/8838cfc17c91ee0d21aab5ecc1572b11c8176931/how-to-guide.pdf)

Мастер сервер для работы с данными полученными из [MoexAlgo](https://github.com/moexalgo/moexalgo/tree/main)

[Предсказания временных рядов](https://github.com/sergeycommit/AlgoPack_time_series)

[Исходные коды микросервисов пайплайна](https://github.com/powerlife000/moex_hackaton/)

[Репозиторий Web UI](https://github.com/Innosan/go_algo_web)

[Исходные коды платфомы на python для торговли на Московской бирже (MOEX)](https://github.com/powerlife000/moex_trading_system)

Перечень скриптов микросервисов:   
- data_markup.py		Оценка потенциальной доходности торговли и инвестиций (тестирование гипотез разметки данных).
- data_gen.py			Генерация датасетов
- edu_neural.py			Обучение нейронных сетей
- calc_profit.py		Оценка доходности нейронных сетей (бек тесты)
- calc_signals.py		Генерация торговых и инвестиционных сигналов

## Установка и настройка базы PostgreSQL

### Установка PostgreSQL

#### Windows
1. Скачайте установщик на сайте: https://www.postgresql.org/download/windows/
2. Запустите .exe файл и пройдите основные шаги по установке.
3. Stack Builder не требуется запускать. Уберите галочку и нажмите Finish
4. В папке PostgreSQL 13 выберите и запустите приложение pgAdmin 4.
5. Задайте пароль для административной панели, например, postgres.
6. Произойдет подключение к серверу по указанному при установке паролю. После чего появится одна предустановленная база данных postgres.
7. Создайте свою базу данных.
   1. Выберите стандартную базу данных postgres и нажмите на нее правой кнопкой мыши.
   2. В появившемся меню нажмите на пункт Query Tool.
      В центральной части программы откроется поле для ввода кода SQL.

       ```sql
          create database <dbname>
       ```
   3. Нажмите на кнопку выполнения кода
#### Linux (Ubuntu)
1. Скачайте и установите PostgreSQL используя следующие команды.
```console
$ sudo apt update
$ sudo apt install postgresql postgresql-contrib
$ sudo systemctl start postgresql.service
$ sudo systemctl status postgresql.service
```
2. Создайте БД
```console
$ sudo -u postgres psql -с "create database <dbname>"
```  
3. Проверьте созданную базу данных
```console
$ sudo -u postgres psql -l
                                  List of databases
    Name    |  Owner   | Encoding |   Collate   |    Ctype    
------------+----------+----------+-------------+--------------
 goalgomoex | postgres | UTF8     | en_US.UTF-8 | en_US.UTF-8  
 postgres   | postgres | UTF8     | en_US.UTF-8 | en_US.UTF-8 
(2 rows)
```
Поле успешно установки и настройки PostgreSQL требуется указать данные для подключения в файле конфигурации
Набор параметров для подключения к БД хранится в файле
[application.properties](https://github.com/DaniilVdovin/goalgomoex_master_server/blob/34b2d9a5d46e4674471cf05ead034dbaa14d6add/src/main/resources/application.properties#L1-L4C56)
```properties
spring.datasource.url=jdbc:postgresql://localhost:5432/<dbname>
spring.datasource.username=<username>
spring.datasource.password=<password>
spring.datasource.driverClassName=org.postgresql.Driver
```
### Установка и настройка java
```console
$ sudo apt install openjdk-17-jdk
```
Проверьте установленный пакет java 
```console
$ java -version
```
После успешной установки java можно настраивать и запускать сервер

# Первоначальная настройка сервера
Сервер настраивается редактированием файла [application.properties](https://github.com/DaniilVdovin/goalgomoex_master_server/blob/34b2d9a5d46e4674471cf05ead034dbaa14d6add/src/main/resources/application.properties)

# Запуск сервера

Linux
```console
$ java -jar goalgomoex.jar
```
Windows
```powershell
> java -jar goalgomoex.jar
```

# Документация по API

После успешного старта сервера документация по API доступна по адресу
```console
http://host:8080/swagger-ui/index.html
```

