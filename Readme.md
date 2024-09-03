# Pusto Studio Test Assignment

## [Задание 1](task1)

 см. task1

## [Задание 2](task2)


### Инструкция к заданию 2

### Запуск

1. В директории src создать файл `.env` по примеру `.env.example`:
```
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=postgres
DB_HOST=postgres
DB_PORT=5432

SECRET_KEY=F96!&$^1IA
DEBUG=True
```
2. Установить приложение командой `docker-compose up -d`
3. Установить миграции командой `sh migrate.sh`
4. Заполнить базу данными командой `sh seed.sh`

### Использование

Приложение доступно по адресу `127.0.0.1:8000/`

Есть один эндпоинт, при помощи которого можно экспортировать данные в .csv:
`/prizes/export/`

Призы создаются при обновлении поля is_completed у объекта PlayerLevel
