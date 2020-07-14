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
vadmin.auth_by_username(login, password)  # by login & password
vadmin.auth_by_token(token_type, access_token)  # by token
```

## Методы API

##### `vadmin.get_load_plans(database_id)`
Возвращает список всех [планов загрузки](#loadplan).

```
[<LoadPlan name(1)>, <LoadPlan name(2)>]
```

##### `vadmin.get_load_plan(database_id, load_plan_id)`
Возвращает объект [плана загрузки](#loadplan).


## <a name="loadplan"></a>Объект плана загрузки (`LoadPlan`)
