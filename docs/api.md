# VAdmin API driver for python3

Библиотека позволяет обращаться к VAdmin API при помощи объектно-ориентированной модели python3.

## Установка пакетов

Для удовлетворения зависимостей, воспользуйтесь командой:

```bash
pip3 install -r requirements.txt
```

## Инициализация

Создадим объект-обёртку API - **VAdminAPI**

```python
vadmin_api_host = 'http://84.201.138.2'
database_id = 'demo'
vadmin = VAdminAPI(vadmin_api_host, database_id)
```

## Авторизация

Библиотека предусматривает авторизацию как по данным учётной записи, так и по токену, если он уже известен.

```python
vadmin.auth_by_username(login, password)  # by login & password
vadmin.auth_by_token(token_type, access_token)  # by token
```

## Методы API

##### `vadmin.get_load_plans(with_status=False)`
Возвращает список всех [планов загрузки](#loadplan). Если установлен флаг `with_status`, то [планы загрузки](#loadplan) будут иметь атрибуты `status`, `progress` соответственно.

```
[<LoadPlan name(1)>, <LoadPlan name(2)>]
```

##### `vadmin.get_load_plan_by_id(load_plan_id)`
Возвращает объект [плана загрузки](#loadplan) по его id. `HTTPError(404)`, если такого плана не существует.

##### `vadmin.get_load_plan_by_name(load_plan_name)`
Возвращает объект [плана загрузки](#loadplan) по его имени. `ValueError`, если такого плана не существует.

## <a name="loadplan"></a>Объект плана загрузки (`LoadPlan`)

Объект `LoadPlan` является объектным представлением плана загрузки. Все методы для работы с API, возвращающие планы загрузки, будут возвращать объект `LoadPlan`. Нет необходимости создания объектов `LoadPlan` вручную, тем не менее, такая возможность предусмотрена.

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
Возвращает статус выполнения плана загрузки. `ResourceWarning`, если план содержит ошибки.

##### `plan.get_progress()`
Возвращает прогресс выполнения плана загрузки.

##### `plan.execute(with_prints=True)`
Отправляет на сервер команду начала выполненеия плана загрузки, ожидая завершение выполнения плана загрузки. [`BrokenPlanError`](#errors), если план включает в себя ошибки, препятствующие выполнению плана. `HTTPError`, если API возвращает ошибку **400**. Если флаг `with_prints` установлен, функция ежесекундно выводит в терминал значение прогресса.

##### `plan.start()`
Отправляет на сервер команду начала выполненеия плана загрузки. [`BrokenPlanError`](#errors), если план включает в себя ошибки, препятствующие выполнению плана.

##### `plan.stop()`
Отправляет на сервер команду остановки выполнения плана загрузки.

> Настоятельно **не** рекомендуется использовать атрибуты объекта `LoadPlan`, т.к. атрибуты актуализируются только при вызове специальных методов. Для получения данных, используёте вышеперечисленные методы.

## <a name="errors"></a>Обработка ошибок
Методы библиотеки предусматривают вызов python-исключений в случае возникновения ошибки на стороне API.

* `HTTPError`, если API возвращает код ошибки (404, 400, 500...)
* `BrokenPlanError`, если пользователь предпринял попытку выполнения плана загрузки, содержащего ошибку.
* `Invalid schema` или `Missing schema`, если пользователь допустил ошибку при указании хоста.
