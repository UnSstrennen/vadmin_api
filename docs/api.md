# VAdmin API driver for python3

Библиотека позволяет обращаться к VAdmin API при помощи объектно-ориентированной модели python3.

## Инициализация

Создадим объект-обёртку API - **VAdminAPI**

```python
vadmin_api_host = 'http://84.201.138.2'
vadmin = VAdminAPI(vadmin_api_host)
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

##### `vadmin.get_load_plan(database_id, load_plan_id, with_status=False)`
Возвращает объект [плана загрузки](#loadplan). Если установлен флаг `with_status`, то [планы загрузки](#loadplan) будут иметь атрибуты `status`, `progress` соответственно.

## <a name="loadplan"></a>Объект плана загрузки (`LoadPlan`)

Объект **`LoadPlan`** является объектным представлением плана загрузки. Все методы для работы с API, возвращающие планы загрузки, будут возвращать объект `LoadPlan`. Нет необходимости создания объектов `LoadPlan` вручную, тем не менее, такая возможность предусмотрена.

```python
# id, database_id and name are REQUIRED
plan = LoadPlan({
  'id': 1,
  'database_id': 'demo',
  'name': 'test_plan'
  })
```

##### `plan.get_steps()`
Возвращает список шагов, включенных в программу плана загрузки.

##### `plan.get_status()`
Возвращает статус выполнения плана загрузки.

##### `plan.get_progress()`
Возвращает прогресс (номер этапа) выполнения плана загрузки.

##### `plan.start()`
Отправляет на сервер команду начала выполненеия плана загрузки.

##### `plan.stop()`
Отправляет на сервер команду остановки выполнения плана загрузки.
