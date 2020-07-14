# VAdmin API driver for python3

Библиотека позволяет обращаться к VAdmin API при помощи объектно-ориентированной модели python3.

## Инициализация

Создадим объект-обёртку API - **VAdminAPI**

```python
vadmin = VAdminAPI()
```

## Авторизация

Библиотека предусматривает авторизацию как по данным учётной записи, так и по токену, если он уже известен.

```python
vadmin.auth(login, password)  # by login & password
vadmin.auth(token)  # by token
```

Функция `auth` возвращает `True` или `False` - успех авторизации.

## Методы API

##### `vadmin.get_load_plans(database_id)`

Возвращает список всех планов загрузки.

```json
[
  {
    "id": 0,
    "name": "string"
  }
]
```

##### `vadmin.get_load_plan(database_id, load_plan_id)`
