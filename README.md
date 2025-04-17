
# atomfoxapi

A small Python API of **ATOM** Mobility.



## Installation

Install python >= 9 version and install **atomfoxapi** with pip:

```bash
pip install atomfoxapi
```
For Mac/Linux may need to create a virtual environment (venv):

```bash
python3 -m venv .venv
source .venv/bin/activate
```
## How to use

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
    print(f'Status for vehicle {vehicle.vehicle_number} successfuly changed!')
else:
    print('An error occurred.')

# this script changes the status on vehicle FF0001
# example output:
# Status for vehicle FF0001 successfuly changed!
```

#### How to **send command** to vehicle
```python
import atomfoxapi

atom = atomfoxapi.Atom('Basic ZX...') # Authorization token

vehicles = atom.get_vehicles(search='FF0001') # get vehicle with num FF0001 | return List[]
vehicle = vehicles[0]

response = atom.send_command('UNLOCK', vehicle.id)
if response:
    print(f'Command success sended to {vehicle.vehicle_number}!')
else:
    print(f'An error occurred.')

# this script sends a command to vehicle FF0001
# example output:
# Command success sended to FF0001!
```

#### How to **create task** in vehicle
```python
import atomfoxapi

atom = atomfoxapi.Atom('Basic ZX...') # Authorization token

vehicles = atom.get_vehicles(search='FF0001') # get vehicle with num FF0001 | return List[]
vehicle = vehicles[0]

response = atom.set_task('vehicle is damaged', 'HIGH', 'vehicle not working', vehicle.id)
if response:
    print(f'Task successful created in {vehicle.vehicle_number}!')
else:
    print(f'An error occurred.')

# this script creates a task on the vehicle FF0001
# example output:
# Task successful created in FF0001!
```

#### How to **get alerts**
```python
import atomfoxapi

atom = atomfoxapi.Atom('Basic ZX...') # Authorization token

alerts = atom.get_alerts('LAST_1_DAY') # get alerts for last 1 day | return List[]

for alert in alerts:
    print(f'{alert.vehicle_nr} - {alert.alert_type} | {alert.timestamp}')

# this get alerts for last 1 day
# example output:
# F0001 - NEED_REBALANCING | 17.04.2025 15:28:47
# F0002 - OVERTURNED | 17.04.2025 15:04:43	
```
## Authors

- [mc_c0rp](https://www.github.com/mc-c0rp) - github
- [@mc_c0rp](https://t.me/mc_c0rp) - Telegram


## License

[MIT](https://choosealicense.com/licenses/mit/)
Moldavskie Technologies | 17.04.2025
