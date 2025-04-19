[🇬🇧 English](./README_en.md) | [🇷🇺 Русский](./README_ru.md) | [🇷🇴 Română](./README_ro.md)

# atomfoxapi

Небольшое Python API для **ATOM** Mobility.

## Установка

Установите Python версии >= 3.9 и установите **atomfoxapi** с помощью pip:

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

#### Как **отправить команду** транспортному средству
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

#### Как **получить оповещения**
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

## Авторы

- [mc_c0rp](https://www.github.com/mc-c0rp) - GitHub
- [@mc_c0rp](https://t.me/mc_c0rp) - Telegram

## Лицензия

[MIT](https://choosealicense.com/licenses/mit/)

Moldavskie Technologies | 17.04.2025
