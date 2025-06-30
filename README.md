[🇬🇧 English](./README.md) | [🇷🇺 Русский](./README_ru.md) | [🇷🇴 Română](./README_ro.md)

# atomfoxapi

A small Python API of **ATOM** Mobility.
[Pypi](https://pypi.org/project/atomfoxapi/)

## Installation

Install python >= 3.9 version and install **atomfoxapi** with pip:

```bash
pip install atomfoxapi
```

For Mac/Linux you may need to create a virtual environment (venv):

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## ATOM REST API

#### How to get **all vehicles**:
```python
import atomfoxapi

atom = atomfoxapi.Atom('Basic ZX...') # Authorization token

vehicles = atom.get_vehicles(load_all=True) # load all vehicles (or load_all=False for load 100 vehicles)

for vehicle in vehicles:
    print(f'{vehicle.vehicle_number} - {vehicle.vehicle_battery}%')

# this script will show the charge of all vehicles
# example output:
# F0001 - 51%
# F0002 - 79%...
```

#### How to **set status** to vehicle:
```python
import atomfoxapi

atom = atomfoxapi.Atom('Basic ZX...') # Authorization token

vehicles = atom.get_vehicles(search='FF0001') # get vehicle with num FF0001 (return List[])
vehicle = vehicles[0]

response = atom.set_status('TRANSPORTATION', vehicle.id)
if response:
    print(f'Status for vehicle {vehicle.vehicle_number} successfully changed!')
else:
    print('An error occurred.')

# this script changes the status on vehicle FF0001
# example output:
# Status for vehicle FF0001 successfully changed!
```

#### How to **send command** to vehicle
```python
import atomfoxapi

atom = atomfoxapi.Atom('Basic ZX...') # Authorization token

vehicles = atom.get_vehicles(search='FF0001') # get vehicle with num FF0001 | return List[]
vehicle = vehicles[0]

response = atom.send_command('UNLOCK', vehicle.id)
if response:
    print(f'Command successfully sent to {vehicle.vehicle_number}!')
else:
    print(f'An error occurred.')

# this script sends a command to vehicle FF0001
# example output:
# Command successfully sent to FF0001!
```

#### How to **create task** in vehicle
```python
import atomfoxapi

atom = atomfoxapi.Atom('Basic ZX...') # Authorization token

vehicles = atom.get_vehicles(search='FF0001') # get vehicle with num FF0001 | return List[]
vehicle = vehicles[0]

response = atom.set_task('vehicle is damaged', 'HIGH', 'vehicle not working', vehicle.id)
if response:
    print(f'Task successfully created in {vehicle.vehicle_number}!')
else:
    print(f'An error occurred.')

# this script creates a task on the vehicle FF0001
# example output:
# Task successfully created in FF0001!
```

#### How to **get alerts**
```python
import atomfoxapi

atom = atomfoxapi.Atom('Basic ZX...') # Authorization token

alerts = atom.get_alerts('LAST_1_DAY') # get alerts for last 1 day | return List[]

for alert in alerts:
    print(f'{alert.vehicle_nr} - {alert.alert_type} | {alert.timestamp}')

# this gets alerts for the last day
# example output:
# F0001 - NEED_REBALANCING | 17.04.2025 15:28:47
# F0002 - OVERTURNED | 17.04.2025 15:04:43
```

#### How to **get statistics**
```python
import atomfoxapi

atom = atomfoxapi.Atom('Basic ZX...') # Authorization token

stats = atom.get_statistics()
print(f'Avaliable: {stats.available_vehicles}\nIn use: {stats.in_use_vehicles}\n',
      f'Total: {stats.total_vehicles}\n Maintenance: {stats.in_service_vehicles}\n')

# this sctipt get statistics of vehicles
# example output:
# Avaliable: 444
# In use: 19
# Total: 490
# Maintenance: 30
```

#### How to **get Employee activity log**
```python
import main as atomfoxapi

atom = atomfoxapi.Atom('Basic ZX...') # Authorization token

logs = atom.get_employee_activity_log()

for log in logs:
    print(f'{log.admin_email} - {log.vehicle_nr} | {log.status_from} → {log.status_to}')

# this sctipt get employee activity log of atom
# example output:
# office@foxscooters.md - FF0001 | Maintenance → Available
# office@foxscooters.md - FF0001 | Available → Transportation
```

#### How to **send a notification** to a user:
```python
import atomfoxapi

atom = atomfoxapi.Atom('Basic ZX...') # Authorization token

response = atom.send_notification('title', 'message', 1234567) # send the notification

if response:
    print('Success!')
else:
    print('An error occurred.')

# This script sends a notification to the app for the user with id 1234567
# REQUIRED ROLE: ≥ General manager (the one with access to the Customers tab)
```

## ATOM GBFS

#### How to get **vehicles**:
```python
import atomfoxapi

# ATOM Mobility provides a GBFS URL like:
# https://your-company.rideatom.com/gbfs/v3_0/en/gbfs?id=1337
# For the `url` parameter, provide the part up to /gbfs/v3_0/en/gbfs (keep the domain, e.g., https://your-company.rideatom.com/)
# For the `subaccount` parameter, use the subaccount ID – for example, from ?id=1337 remove ?id= -> you get 1337
# Important note: get_vehicles() in GBFS only returns vehicles that are in Available status (ACTIVE/READY)

gbfs = atomfoxapi.GBFS(url='https://your-company.rideatom.com/', subaccount=1337)  # authenticate to GBFS (replace with your URL and subaccount ID)

vehicles = gbfs.get_vehicles()  # get the list of available vehicles from GBFS (as a list)

for vehicle in vehicles:
    print(f"{vehicle.vehicle_number} - {vehicle.lat}, {vehicle.lon}")
print(f"ALL: {len(vehicles)}")

# Why is this needed? It's a backup solution for unexpected situations. Yes, it gives less data, but it's better than nothing.
# Example output:
# F0001 - 47.031074, 28.838779
# F0002 - 47.031075, 28.838780
# ALL: 2
```

## Authors

- [mc_c0rp](https://www.github.com/mc-c0rp) - GitHub
- [@mc_c0rp](https://t.me/mc_c0rp) - Telegram

## License

[MIT](https://choosealicense.com/licenses/mit/)

last upd 01.07.2025
