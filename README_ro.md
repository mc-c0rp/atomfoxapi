[🇬🇧 English](./README.md) | [🇷🇺 Русский](./README_ru.md) | [🇷🇴 Română](./README_ro.md)

# atomfoxapi

O mică API Python pentru **ATOM** Mobility.
[Pypi](https://pypi.org/project/atomfoxapi/)

## Instalare

Instalați Python versiunea >= 3.9 și instalați **atomfoxapi** cu pip:

```bash
pip install atomfoxapi
```

Pentru Mac/Linux poate fi necesară crearea unui mediu virtual (venv):

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## ATOM REST API

#### Cum să obțineți **toate vehiculele**:
```python
import atomfoxapi

atom = atomfoxapi.Atom('Basic ZX...') # Token de autorizare

vehicles = atom.get_vehicles(load_all=True) # încarcă toate vehiculele (sau load_all=False pentru primele 100)

for vehicle in vehicles:
    print(f'{vehicle.vehicle_number} - {vehicle.vehicle_battery}%')

# acest script va afișa nivelul de încărcare al tuturor vehiculelor
# exemplu de ieșire:
# F0001 - 51%
# F0002 - 79%...
```

#### Cum să **schimbați statusul** vehiculului:
```python
import atomfoxapi

atom = atomfoxapi.Atom('Basic ZX...') # Token de autorizare

vehicles = atom.get_vehicles(search='FF0001') # obține vehiculul FF0001 (returnează List[])
vehicle = vehicles[0]

response = atom.set_status('TRANSPORTATION', vehicle.id)
if response:
    print(f'Stătutul vehiculului {vehicle.vehicle_number} a fost schimbat cu succes!')
else:
    print('A apărut o eroare.')

# acest script schimbă statusul vehiculului FF0001
# exemplu de ieșire:
# Stătutul vehiculului FF0001 a fost schimbat cu succes!
```

#### Cum să **trimiteți o comandă** vehiculului
```python
import atomfoxapi

atom = atomfoxapi.Atom('Basic ZX...') # Token de autorizare

vehicles = atom.get_vehicles(search='FF0001') # obține vehiculul FF0001 | returnează List[]
vehicle = vehicles[0]

response = atom.send_command('UNLOCK', vehicle.id)
if response:
    print(f'Comanda a fost trimisă cu succes către {vehicle.vehicle_number}!')
else:
    print('A apărut o eroare.')

# acest script trimite o comandă vehiculului FF0001
# exemplu de ieșire:
# Comanda a fost trimisă cu succes către FF0001!
```

#### Cum să **creați task** vehiculului
```python
import atomfoxapi

atom = atomfoxapi.Atom('Basic ZX...') # Token de autorizare

vehicles = atom.get_vehicles(search='FF0001') # obține vehiculul FF0001 | returnează List[]
vehicle = vehicles[0]

response = atom.set_task('vehicle is damaged', 'HIGH', 'vehicle not working', vehicle.id)
if response:
    print(f'Task creat cu succes în vehiculul {vehicle.vehicle_number}!')
else:
    print('A apărut o eroare.')

# acest script creează un task pentru vehiculul FF0001
# exemplu de ieșire:
# Task creat cu succes în vehiculul FF0001!
```

#### Cum să **obțineți alertele**
```python
import atomfoxapi

atom = atomfoxapi.Atom('Basic ZX...') # Token de autorizare

alerts = atom.get_alerts('LAST_1_DAY') # obține alertele din ultima zi | returnează List[]

for alert in alerts:
    print(f'{alert.vehicle_nr} - {alert.alert_type} | {alert.timestamp}')

# acest script obține alertele din ultima zi
# exemplu de ieșire:
# F0001 - NEED_REBALANCING | 17.04.2025 15:28:47
# F0002 - OVERTURNED | 17.04.2025 15:04:43
```

#### Cum să **obții statistici**
```python
import atomfoxapi

atom = atomfoxapi.Atom('Basic ZX...') # Token de autorizare

stats = atom.get_statistics()
print(f'Avaliable: {stats.available_vehicles}\nIn use: {stats.in_use_vehicles}\n',
      f'Total: {stats.total_vehicles}\n Maintenance: {stats.in_service_vehicles}\n')

# acest script obține statistici despre vehicule
# exemplu de ieșire:
# Avaliable: 444
# In use: 19
# Total: 490
# Maintenance: 30
```

#### Cum să **obții Employee activity log** din Dashboard
```python
import main as atomfoxapi

atom = atomfoxapi.Atom('Basic ZX...') # Token de autorizare

logs = atom.get_employee_activity_log()

for log in logs:
    print(f'{log.admin_email} - {log.vehicle_nr} | {log.status_from} → {log.status_to}')

# acest script obține employee activity log din Atom
# exemplu de ieșire:
# office@foxscooters.md - FF0001 | Maintenance → Available
# office@foxscooters.md - FF0001 | Available → Transportation
```

#### Cum să **trimiți o notificare** unui utilizator:
```python
import atomfoxapi

atom = atomfoxapi.Atom('Basic ZX...') # Token de autorizare

response = atom.send_notification('title', 'message', 1234567) # trimite notificarea

if response:
    print('Succes!')
else:
    print('A apărut o eroare.')

# Acest script trimite o notificare în aplicație pentru utilizatorul cu id-ul 1234567
# ROL NECESAR: ≥ General manager (cel care are acces la fila Customers)
```

## ATOM GBFS

#### Cum să obțineți **vehiculele**:
```python
import atomfoxapi

# ATOM Mobility oferă un URL pentru GBFS similar cu:
# https://your-company.rideatom.com/gbfs/v3_0/en/gbfs?id=1337
# Pentru parametrul `url`, trebuie transmisă partea URL-ului până la /gbfs/v3_0/en/gbfs (păstrați domeniul, ex: https://your-company.rideatom.com/)
# Pentru parametrul `subaccount`, trebuie transmis ID-ul subcontului – de exemplu, din ?id=1337 eliminăm ?id= -> obținem 1337
# Este important de menționat: get_vehicles() din GBFS returnează doar vehiculele care sunt în status Available (ACTIVE/READY)

gbfs = atomfoxapi.GBFS(url='https://your-company.rideatom.com/', subaccount=1337)  # ne conectăm la GBFS (înlocuiți cu URL-ul și ID-ul vostru de subcont)

vehicles = gbfs.get_vehicles()  # obținem lista vehiculelor disponibile din GBFS (listă)

for vehicle in vehicles:
    print(f"{vehicle.vehicle_number} - {vehicle.lat}, {vehicle.lon}")
print(f"TOATE: {len(vehicles)}")

# De ce este necesar acest script? Este o soluție de rezervă pentru situații neprevăzute. Da, conține mai puține date, dar e mai bine decât nimic.
# Exemplu de rezultat:
# F0001 - 47.031074, 28.838779
# F0002 - 47.031075, 28.838780
# TOATE: 2
```

## Autori

- [mc_c0rp](https://www.github.com/mc-c0rp) - GitHub
- [@mc_c0rp](https://t.me/mc_c0rp) - Telegram

## Licență

[MIT](https://choosealicense.com/licenses/mit/)

last upd 01.07.2025 (переведено через чат гпт)
