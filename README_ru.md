[🇬🇧 English](./README.md) | [🇷🇺 Русский](./README_ru.md) | [🇷🇴 Română](./README_ro.md)

# atomfoxapi

Небольшое Python API для **ATOM** Mobility.
[Pypi](https://pypi.org/project/atomfoxapi/)

## Установка

Установите Python версии >= 3.9 и **atomfoxapi** с помощью pip:

```bash
pip install atomfoxapi
```

Для Mac/Linux может потребоваться создание виртуального окружения (venv):

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## Использование

#### Как получить **все транспортные средства**:
```python
import atomfoxapi

atom = atomfoxapi.Atom('Basic ZX...') # Токен авторизации

vehicles = atom.get_vehicles(load_all=True) # загрузить все транспортные средства (или load_all=False для первых 100)

for vehicle in vehicles:
    print(f'{vehicle.vehicle_number} - {vehicle.vehicle_battery}%')

# этот скрипт покажет заряд всех транспортных средств
# пример вывода:
# F0001 - 51%
# F0002 - 79%...
```

#### Как **установить статус** транспортного средства:
```python
import atomfoxapi

atom = atomfoxapi.Atom('Basic ZX...') # Токен авторизации

vehicles = atom.get_vehicles(search='FF0001') # получить транспортное средство FF0001 (возвращает List[])
vehicle = vehicles[0]

response = atom.set_status('TRANSPORTATION', vehicle.id)
if response:
    print(f'Статус транспортного средства {vehicle.vehicle_number} успешно изменён!')
else:
    print('Произошла ошибка.')

# этот скрипт меняет статус транспортного средства FF0001
# пример вывода:
# Статус транспортного средства FF0001 успешно изменён!
```

#### Как **отправить команду** на транспортное средство
```python
import atomfoxapi

atom = atomfoxapi.Atom('Basic ZX...') # Токен авторизации

vehicles = atom.get_vehicles(search='FF0001') # получить транспортное средство FF0001 | возвращает List[]
vehicle = vehicles[0]

response = atom.send_command('UNLOCK', vehicle.id)
if response:
    print(f'Команда успешно отправлена на {vehicle.vehicle_number}!')
else:
    print('Произошла ошибка.')

# этот скрипт отправляет команду на транспортное средство FF0001
# пример вывода:
# Команда успешно отправлена на FF0001!
```

#### Как **создать таск** в транспортном средстве
```python
import atomfoxapi

atom = atomfoxapi.Atom('Basic ZX...') # Токен авторизации

vehicles = atom.get_vehicles(search='FF0001') # получить транспортное средство FF0001 | возвращает List[]
vehicle = vehicles[0]

response = atom.set_task('vehicle is damaged', 'HIGH', 'vehicle not working', vehicle.id)
if response:
    print(f'Таск успешно создан в транспортном средстве {vehicle.vehicle_number}!')
else:
    print('Произошла ошибка.')

# этот скрипт создаёт таск для транспортного средства FF0001
# пример вывода:
# Таск успешно создан в транспортном средстве FF0001!
```

#### Как **получить алерты**
```python
import atomfoxapi

atom = atomfoxapi.Atom('Basic ZX...') # Токен авторизации

alerts = atom.get_alerts('LAST_1_DAY') # получить оповещения за последний день | возвращает List[]

for alert in alerts:
    print(f'{alert.vehicle_nr} - {alert.alert_type} | {alert.timestamp}')

# этот скрипт получает оповещения за последний день
# пример вывода:
# F0001 - NEED_REBALANCING | 17.04.2025 15:28:47
# F0002 - OVERTURNED | 17.04.2025 15:04:43
```

#### Как **получить статистику** с главной страницы Dashboard
```python
import atomfoxapi

atom = atomfoxapi.Atom('Basic ZX...') # Токен авторизации

stats = atom.get_statistics()
print(f'Avaliable: {stats.available_vehicles}\nIn use: {stats.in_use_vehicles}\n',
      f'Total: {stats.total_vehicles}\n Maintenance: {stats.in_service_vehicles}\n')

# этот скрипт получает статистику по транспортным средствам
# пример вывода:
# Avaliable: 444
# In use: 19
# Total: 490
# Maintenance: 30
```

#### Как **получить Employee activity log** из Dashboard
```python
import main as atomfoxapi

atom = atomfoxapi.Atom('Basic ZX...') # Токен авторизации

logs = atom.get_employee_activity_log()

for log in logs:
    print(f'{log.admin_email} - {log.vehicle_nr} | {log.status_from} → {log.status_to}')

# этот скрипт получает employee activity log из Атома
# пример вывода:
# office@foxscooters.md - FF0001 | Maintenance → Available
# office@foxscooters.md - FF0001 | Available → Transportation
```

## Авторы

- [mc_c0rp](https://www.github.com/mc-c0rp) - GitHub
- [@mc_c0rp](https://t.me/mc_c0rp) - Telegram

## Лицензия

[MIT](https://choosealicense.com/licenses/mit/)

Moldavskie Technologies | 17.04.2025
