"""
ATOM MOBILITY API V2
by mc_c0rp for FAST FOX
Version: R12

Version Description:
T - TEST
D - DEVELOPMENT
R - RELEASE

Version Log:
T01 - первые наброски         
T02 - почти готовая основа    
R01 - фикс багов и первый релиз в PyPI (v1.0.4)
R02 - добавлены функции delete_task и done_task (v1.1.0)
R03 - добавлен параметр load_all в get_alerts() (v1.1.6)
R04 - фикс подсказок для IDE (v1.1.8)
R05 - добавлена функция get_statistics() и get_employee_activity_log, также автоматическая установка зависимостей (v1.2.1)
R06 - добавлена функция get_iots() (v1.2.3)
R07 - добавлена функция get_new_iot_detected() и send_notification(); функции типа set теперь возвращают False при неудачном запросе | pypi ver. 1.2.4 / 23.04.2025
R08 - удален print ответа от сервера в функции get_rides() | pypi ver. 1.2.5 / 06.05.2025
R09 - добавлена функция find_users | pypi ver. 1.2.6 / 08.05.2025.
R10 - добавлена функция get_task_manager_info и get_tasks_manager | pypi ver. 1.2.7 / 11.05.2025
R11 - исправлен баг с get_statistics() | pypi ver. 1.2.8 / 30.05.2025
R12 - добавлена функция get_vehicle_activity | pypi ver. 1.3.0 / 26.06.2025
"""

from .main import Atom, commands, tasks, tasks_types
from .main import (
    Navigation,
    Iot,
    RidesItem,
    VehiclesItem,
    AlertItem,
    Tasks,
    Statistics,
    EmployeeActivityLogStatus,
    ManageIot,
    TaskManagerInfo,
    TasksManagerResponse,
    TaskManagerItem,
    VehicleActivity
)

__all__ = [
    "Atom",
    "commands",
    "tasks",
    "tasks_types",
    "Navigation",
    "Iot",
    "RidesItem",
    "VehiclesItem",
    "AlertItem",
    "Tasks",
    "Statistics",
    "EmployeeActivityLogStatus",
    "ManageIot",
    "TaskManagerInfo",
    "TasksManagerResponse",
    "TaskManagerItem",
    "VehicleActivity"
]
