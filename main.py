# ATOM MOBILITY API V2
# by mc_c0rp for FAST FOX
# version R07

# version description:
# T - TEST
# D - DEVELOPMENT
# R - RELEASE

# version log:
# T01 - первые наброски                                                 # R01 - фикс багов и первый релиз в pypi | pypi ver. 1.0.4
# T02 - почти готовая основа                                            # R02 - добавлены функции delete_task; done_task. | pypi ver. 1.1.0
# R03 - добавлен параметр load_all в get_alerts() | pypi ver. 1.1.6     # R04 - фикс подсказок для IDE | pypi ver. 1.1.8
# R05 - добавлена функция get_statistics() и get_employee_activity_log, также автоматическая установка зависимостей | pypi ver. 1.2.1
# R06 - добавлена функция get_iots() | pypi ver. 1.2.3 / 23.04.2025
# R07 - добавлена функция get_new_iot_detected() и send_notification(); функции типа set теперь возвращают False при неудачном запросе | pypi ver. 1.2.4 / 23.04.2025
# R08 - удален print ответа от сервера в функции get_rides() | pypi ver. 1.2.5 / 06.05.2025
# R09 - добавлена функция find_users | pypi ver. 1.2.6 / 08.05.2025.    # R10 - добавлена функция get_task_manager_info и get_tasks_manager | pypi ver. 1.2.7 / 11.05.2025
# R11 - исправлен баг с get_statistics() | pypi ver. 1.2.8 / 30.05.2025 # R12 - добавлена функция get_vehicle_activity | pypi ver. 1.3.0 / 26.06.2025

try:
    import requests
    from typing import Literal, List, Optional, Union
    from datetime import datetime, timedelta
    from pydantic import BaseModel
except ImportError:
    import os
    os.system('pip install requests pydantic')


# -------------------------------
#  Вспомогательные структуры и модели
# -------------------------------

# OKAI ES400A
commands = Literal[
    "UNLOCK", "LOCK", "UNLOCK_ENCHANTED", "UNLOCK_MECHANICAL_LOCK", "LOCK_MECHANICAL_LOCK",
    "REBOOT", "POWER_OFF", "UPDATE_GEO_INFO", "WARN", "HEADLIGHT_ON", "HEADLIGHT_OFF",
    "REARLIGHT_ON", "REARLIGHT_ON_FORCED", "REARLIGHT_OFF", "ENGINE_ON", "ENGINE_OFF",
    "WIRELESS_CHARGING_ON", "WIRELESS_CHARGING_OFF", "SET_DISPLAY_UNIT_YD", "SET_DISPLAY_UNIT_KM",
    "MODE_NORMAL", "MODE_SPORT", "MAX_SPEED_LIMIT_FROM_0_TO_63_KM/H", "SET_ALARM_INTERVAL_FROM_5_TO_3600_SECONDS",
    "SET_VIBRATION_ALARM_INTERVAL_FROM_0_TO_300_SECONDS", "SET_NEVER_TURN_OFF_GPS", "SET_TURN_OFF_GPS_WHEN_NOT_NEEDED",
    "AGPS_MODE_ON", "AGPS_MODE_OFF", "BACKUP_VOICE_PLAY_ENABLED", "BACKUP_VOICE_PLAY_DISABLED", "VOICE_PLAY_ENABLED",
    "VOICE_PLAY_DISABLED", "POWER_OFF_ENABLED", "POWER_OFF_DISABLED", "SET_VOLUME_FROM_0_TO_7",
    "SET_ALARM_VOLUME_FROM_0_TO_7", "GREEN_LED_ENABLED", "GREEN_LED_DISABLED", "LED_MODE_CONSTANT",
    "LED_MODE_FLASHES", "LED_BLINK_FREQUENCY_FROM_20_TO_100", "MECHANICAL_LOCK_ENABLED",
    "MECHANICAL_LOCK_DISABLED", "ELECTRONIC_BELL_ENABLED", "ELECTRONIC_BELL_DISABLED",
    "NFC_WORK_MODE_ENABLED", "NFC_WORK_MODE_DISABLED", "SCOOTER_BATTERY_HEATING_ON",
    "SCOOTER_BATTERY_HEATING_OFF", "SET_MECHANICAL_LOCK_TYPE_BATTERY_LOCK_A",
    "SET_MECHANICAL_LOCK_TYPE_BATTERY_LOCK_B", "SET_MECHANICAL_LOCK_TYPE_PILE_LOCK",
    "SET_MECHANICAL_LOCK_TYPE_BASKET_LOCK", "SET_MOVE_DETECTION_NON_MOVEMENT_DURATION_FROM_1_TO_255",
    "SET_MOVE_DETECTION_MOVEMENT_DURATION_FROM_1_TO_50", "SET_MOVE_DETECTION_SENSITIVITY_FROM_2_TO_19",
    "SET_VEHICLE_IN_NORMAL_MODE", "SET_VEHICLE_IN_TEST_MODE", "SET_DEFAULT_REPORT_INTERVAL",
    "SET_5_SEC_REPORT_INTERVAL", "SET_ALARM_REPORT_INTERVAL", "REQUEST_CONFIGURATION",
    "REQUEST_VER_CONFIGURATION", "REQUEST_CANVER_CONFIGURATION", "ENABLE_BLE_UNLOCK",
    "DISABLE_BLE_UNLOCK", "UPDATE_BLE_BROADCAST_NAME", "ENABLE_NFC_WORK_MODE", "DISABLE_NFC_WORK_MODE",
    "SET_BATTERY_LOCK_ALARM_TIMES", "UPDATE_CUSTOMER_ID", "SET_NFC_TAG_ID", "SET_BLE_PASSWORD",
    "START_UPDATE_FIRMWARE", "START_UPDATE_BATTERY_FIRMWARE", "START_UPDATE_BATTERY_LOCK_FIRMWARE",
    "STOP_UPDATE_FIRMWARE", "START_UPDATE_RING_AUDIO_FILE", "CONFIGURE_HELMET_BOX_SELECTION_1",
    "START_UPDATE_LOCK_AUDIO", "CONFIGURE_HELMET_BOX_SELECTION_2", "START_UPDATE_UNLOCK_AUDIO",
    "START_UPDATE_ALARM_AUDIO", "UNLOCK_HELMET_BOX", "BLACKLIST_NETWORK_CUSTOM_1"
]

tasks = {
    'vehicle is damaged': 123,
    'problem with iot': 124,
    'maintenance required': 125,
    'check-up required': 126,
    'battery swap': 127,
    'battery charging required': 128,
    'fueling required': 129,
    'rebalance (collect)': 130,
    'rebalance (deploy)': 131,
    'out of parking zone': 132,
    'located in no-go zone': 133,
    'other': 134
}

tasks_types = Literal[
    'vehicle is damaged',
    'problem with iot',
    'maintenance required',
    'check-up required',
    'battery swap',
    'battery charging required',
    'fueling required',
    'rebalance (collect)',
    'rebalance (deploy)',
    'out of parking zone',
    'located in no-go zone',
    'other'
]

class Navigation(BaseModel):
    longitude: float
    latitude: float

class Iot(BaseModel):
    battery: Optional[int] = None
    id: Optional[int] = None
    imei: Optional[str] = None
    phone_number: Optional[str] = None
    last_update: Optional[str] = None

class RidesItem(BaseModel):
    id: int
    start_time: str
    end_time: str
    vehicle_number: str
    vehicle_id: int
    kilometers: float
    time: str
    price: str
    charged_balance: str
    charged_bonus: str
    feedback: Union[str, int]
    comment: str
    end_location: Navigation
    image: Optional[Union[List[str], str]]
    user_end_location: Optional[Navigation]
    user_id: int
    user_name: str
    phone: str
    email: str
    vehicle_model_id: int

class VehiclesItem(BaseModel):
    id: int
    vehicle_number: str
    vehicle_battery: float
    navigation: Navigation
    history_link: Optional[str]
    iot: Optional[Iot]
    total_rides: int
    old_status: str
    last_park_photo: Union[List[str], str]
    last_park_date: Optional[str]
    qr: str
    selected_status: str
    selected_model: int
    selected_subaccount: int
    lock: Optional[str]

class AlertItem(BaseModel):
    timestamp: str
    vehicle_id: int
    alert_type: str
    subaccount_id: int
    vehicle_nr: str

class Tasks(BaseModel):
    date: str
    id: int
    priority: str
    stage: str
    type: str

class Statistics(BaseModel):
    available_vehicles: int
    in_use_vehicles: int
    charging_vehicles: int
    in_service_vehicles: int
    total_vehicles: int
    all_vehicles: int
    discharged_vehicles: int
    needs_investigation_vehicles: int
    stolen_vehicles: int
    not_ready_vehicles: int
    transportation_vehicles: int
    storage_vehicles: int
    rides_today: Optional[int] = None
    rides_yesterday: Optional[int] = None
    average_rides: Optional[int] = None
    customers_today: Optional[int] = None
    customers_yesterday: Optional[int] = None
    average_customers: Optional[int] = None
    rides_revenue_today: Optional[str] = None
    rides_revenue_yesterday: Optional[str] = None
    topup_today: Optional[str] = None
    topup_yesterday: Optional[str] = None
    active_vehicles_with_errors: List[str] = []
    currency_symbol: str
    currency_code: str
    total_vehicle_error_count: int = 0
    tasks_today: int = 0
    tasks_yesterday: int = 0
    open_tasks: int = 0
    damages_today: int = 0
    damages_yesterday: int = 0
    open_damages: int = 0
    rebalancing_vehicles: int = 0
    subscriptions_revenue_today: Optional[str] = None
    subscriptions_revenue_yesterday: Optional[str] = None

class EmployeeActivityLogStatus(BaseModel):
    admin_email: str
    admin_id: int
    coordinates: str # GOOGLE LINK!!!
    date: str
    last_iot_update_date: str
    last_ride_date: str
    status_from: str
    status_to: str
    vehicle_battery: str # С СИМВОЛОМ %!!!!!
    vehicle_id: int
    vehicle_nr: str

class ManageIot(BaseModel):
    id: int
    imei: str
    model: str
    phone_prefix: int
    phone: str
    battery: int
    last_update: str
    is_integrated: Union[str, bool]
    allows_tcp_commands: Union[str, bool]
    subaccount_id: int

class TaskManagerItem(BaseModel):
    id: int
    date: str
    type: str
    priority: str
    stage: str
    start_date: str
    end_date: str
    vehicle_nr: str
    vehicle_id: int
    imei: str
    status: str
    created_by: str
    marked_as_done_date: str
    marked_as_done_by: str

class TasksManagerResponse(BaseModel):
    bookmark_next: str
    bookmark_previous: str
    has_next_page: bool
    has_previous_page: bool
    data: List[TaskManagerItem]

class FindUser(BaseModel):
    id: int
    email: str
    phone: str
    name: str
    document: str
    document_addition: str
    document_number: str
    saved_card: bool
    wallet: int
    debt: int
    rides: int
    avg_feedback: str
    blocked: bool
    currency_symbol: str
    currency_code: str

class TaskManagerInfo(BaseModel):
    type: str
    priority: str
    start_date: str
    end_date: str
    description: str

class VehicleActivity(BaseModel):
    date: str
    user: str
    action: str
    description: str # always '-', hui ego znaet pochemu

class Atom:
    def __init__(self, token: str):
        """
        :param token: ATOM Mobility token
        """
        self.token = token

    def get_rides(
        self,
        ride_status: Literal["ENDED", "ACTIVE"] = "ENDED",
        search: str = "",
        comments: Literal["ALL", "AVAILABLE"] = "AVAILABLE",
        distance_from: int = 0,
        distance_to: int = 10,
        duration_from: int = 0,
        duration_to: int = 100,
        feedback_from: int = 0,
        feedback_to: int = 5,
        models: List[int] = [0],
        page_length: int = 100,
        today: bool = False
    ) -> List[RidesItem]:
        url = 'https://app.rideatom.com/api/v2/admin/rides'
        headers = {"authorization": self.token}
        if today:
            now = datetime.now()
            data = {
                "ride_status": ride_status,
                "page_length": page_length,
                "search": search,
                "comments": comments,
                "distance": {"from": distance_from, "to": distance_to},
                "duration": {"from": duration_from, "to": duration_to},
                "feedback": {"from": feedback_from, "to": feedback_to},
                "models": models,
                "use_page_by_page": True,
                "date_range": {"from": now.strftime("%Y-%m-%d"), "to": now.strftime("%Y-%m-%d")}                
            }
        else:
            data = {
                "ride_status": ride_status,
                "page_length": page_length,
                "search": search,
                "comments": comments,
                "distance": {"from": distance_from, "to": distance_to},
                "duration": {"from": duration_from, "to": duration_to},
                "feedback": {"from": feedback_from, "to": feedback_to},
                "models": models,
                "use_page_by_page": True
            }
        resp = requests.post(url, json=data, headers=headers)
        resp.raise_for_status()
        rides_data = resp.json().get('data', [])
        rides: List[RidesItem] = []
        for ride in rides_data:
            if ride_status != 'ACTIVE':
                ride['kilometers'] = float(str(ride['kilometers']).replace(' km', ''))
            rides.append(RidesItem.model_validate(ride))
        return rides

    def get_vehicles(
        self,
        filter: List[Literal[
            "ALL", "ACTIVE", "IN_USE", "RESERVED", "DISCHARGED", "CHARGING", "NEED_INVESTIGATION",
            "NEED_SERVICE", "REBALANCING", "TRANSPORTATION", "STORAGE", "NOT_READY", "STOLEN",
            "DEPRECATED"
        ]] = ["ALL"],
        task_and_damages: List[Literal[
            "ALL", "TASKS_TODO", "TASKS_OVERDUE", "DAMAGE_REPORTS_IN_REVIEW", "DAMAGE_REPORTS_APPROVED"
        ]] = ["ALL"],
        search: str = "",
        page: int = 1,
        battery_from: int = 0,
        battery_to: int = 100,
        iot_battery_from: int = 0,
        iot_battery_to: int = 100,
        last_ride_from: int = 0,
        last_ride_to: int = 168,
        total_rides_from: int = 0,
        total_rides_to: int = 100,
        last_iot_signal_from: int = 0,
        last_iot_signal_to: int = 200,
        models: List[int] = [0],
        page_length: int = 100,
        load_all: bool = False
    ) -> List[VehiclesItem]:
        url = 'https://app.rideatom.com/api/v2/admin/vehicles'
        headers = {"authorization": self.token}
        data = {
            "page": page,
            "page_length": page_length,
            "search": search,
            "filter": filter,
            "models": models,
            "tasks_and_damages": task_and_damages,
            "sliders": [
                {"from": battery_from, "to": battery_to, "key": "vehicle_battery"},
                {"from": iot_battery_from, "to": iot_battery_to, "key": "iot_battery"},
                {"from": last_iot_signal_from, "to": last_iot_signal_to, "key": "last_iot_signal"},
                {"from": last_ride_from, "to": last_ride_to, "key": "last_ride"},
                {"from": total_rides_from, "to": total_rides_to, "key": "total_rides"}
            ]
        }
        all_data: List[dict] = []
        while True:
            resp = requests.post(url, json=data, headers=headers)
            resp.raise_for_status()
            page_data = resp.json().get('data', [])
            all_data.extend(page_data)
            if not load_all or not resp.json().get('has_next_page'):
                break
            data['page'] += 1
        vehicles = [VehiclesItem.model_validate(item) for item in all_data]
        return vehicles
    
    def find_users(
        self,
        filter: List[Literal[
            "ALL", "WITH_DEBT", "BLOCKED", "WITH_SAVED_CARD", "WITHOUT_SAVED_CARD", "DELETION_REQUESTED"
        ]] = ["ALL"],
        search: str = "",
        page_length: int = 100,
        wallet_from: int = 0,
        wallet_to: int = 100,
        rides_from: int = 0,
        rides_to: int = 100,
        last_ride_from: int = 0,
        last_ride_to: int = 168,
        feedback_from: int = 0,
        feedback_to: int = 5
    ) -> List[FindUser]:
        url = 'https://app.rideatom.com/api/v2/admin/users'
        headers = {"authorization": self.token}
        data = {
            "page_length": page_length,
            "search": search,
            "filter": filter,
            "sliders": [
                {"from": wallet_from, "to": wallet_to, "key": "wallet"},
                {"from": rides_from, "to": rides_to, "key": "rides"},
                {"from": feedback_from, "to": feedback_to, "key": "feedback"},
                {"from": last_ride_from, "to": last_ride_to, "key": "last_ride"}
            ],
            "use_page_by_page": True
        }
        all_data: List[dict] = []
        resp = requests.post(url, json=data, headers=headers)
        resp.raise_for_status()
        page_data = resp.json().get('data', [])
        all_data.extend(page_data)
        for data in all_data:
            if data["saved_card"] == "Yes":
                data['saved_card'] = True
            else:
                data['saved_card'] = False
        users = [FindUser.model_validate(item) for item in all_data]
        return users
    
    def get_iots(
        self,
        filter: Literal[
            "ALL", "ONLY_USED", "NOT_USED", "INACTIVE_1_DAY"
        ] = "ALL",
        search: str = "",
        page: int = 1,
        page_length: int = 100,
        load_all: bool = False
    ) -> List[ManageIot]:
        url = 'https://app.rideatom.com/api/v2/admin/trackers'
        headers = {"authorization": self.token}
        data = {
            "page": page,
            "page_length": page_length,
            "search": search,
            "filter": filter
        }
        all_data: List[dict] = []
        while True:
            resp = requests.post(url, json=data, headers=headers)
            resp.raise_for_status()
            page_data = resp.json().get('data', [])
            all_data.extend(page_data)
            if not load_all or not resp.json().get('has_next_page'):
                break
            data['page'] += 1
        iots = [ManageIot.model_validate(item) for item in all_data]
        return iots

    def get_alerts(
        self,
        filter: Literal["LAST_1_DAY", "LAST_2_DAYS", "LAST_7_DAYS", "LAST_30_DAYS"] = 'LAST_1_DAY',
        search: str = "",
        page: int = 1,
        page_length: int = 100,
        load_all: bool = False
    ) -> List[AlertItem]:
        url = 'https://app.rideatom.com/api/v2/admin/vehicle-alerts'
        headers = {"authorization": self.token}
        data = {"filter": filter, "search": search, "page": page, "page_length": page_length}
        all_alerts: List[dict] = []
        while True:
            resp = requests.post(url, json=data, headers=headers)
            resp.raise_for_status()
            json_resp = resp.json()
            all_alerts.extend(json_resp.get('data', []))
            if not load_all or not json_resp.get('has_next_page'):
                break
            data['page'] += 1
        return [AlertItem.model_validate(a) for a in all_alerts]

    def get_employee_activity_log(
        self,
        search: str = "",
        page_length: int = 100,
    ) -> List[EmployeeActivityLogStatus]:
        url = 'https://app.rideatom.com/api/v2/admin/employee-activity-log'
        headers = {"authorization": self.token}
        data = {"filter": "VEHICLE_STATUS_CHANGE", "search": search, "page_length": page_length} # потом добавлю остальные фильтры
        resp = requests.post(url, json=data, headers=headers)
        resp.raise_for_status()
        logs = resp.json().get('data', [])

        return [EmployeeActivityLogStatus.model_validate(a) for a in logs]


    def get_tasks(
        self,
        vehicle_id: int,
        page: int = 1,
        page_length: int = 100
    ) -> List[Tasks]:
        url = 'https://app.rideatom.com/api/v2/admin/vehicle/tasks'
        headers = {"authorization": self.token}
        data = {"vehicle_id": vehicle_id, "page": page, "page_length": page_length}
        resp = requests.post(url, json=data, headers=headers)
        resp.raise_for_status()
        tasks_data = resp.json().get('data', [])
        return [Tasks.model_validate(t) for t in tasks_data]
    
    def get_task_manager_info(self, entity: int) -> TaskManagerInfo:
        url = 'https://app.rideatom.com/api/v2/admin/task-manager/review'
        headers = {"authorization": self.token}
        params = {"entity_id": entity}
        resp = requests.get(url, params=params, headers=headers)
        resp.raise_for_status()
        task_data = resp.json()
        return TaskManagerInfo.model_validate(task_data)
    
    # Новые классы для подсказок (автодополнения) при работе с задачами

    # Изменённый метод get_tasks_manager
    def get_tasks_manager(
        self,
        search: str = "",
        task_stages: List[Literal["ALL", "TODO"]] = ["ALL"],
        task_types: List[str] = ["ALL"],
        task_priorities: List[Literal["ALL", "LOW", "MEDIUM", "HIGH"]] = ["ALL"],
        vehicle_statuses: List[str] = ["ALL"],
        vehicle_model_ids: List[int] = [0],
        date_range_from: str = '',
        date_range_to: str = '',
        page_length: int = 100,
        page_bookmark: str = ""
    ) -> TasksManagerResponse:
        if date_range_from == '':
            print("Data range is empty!")
            exit()
        if date_range_to == '':
            print("Data range is empty!")
            exit()
        url = 'https://app.rideatom.com/api/v2/admin/task-manager'
        headers = {"authorization": self.token}
        data = {
            "search": search,
            "task_stages": task_stages,
            "task_types": task_types,
            "task_priorities": task_priorities,
            "vehicle_statuses": vehicle_statuses,
            "vehicle_model_ids": vehicle_model_ids,
            "date_range": {"from": date_range_from, "to": date_range_to},
            "page_length": page_length,
            "page_bookmark": page_bookmark
        }
        resp = requests.post(url, json=data, headers=headers)
        resp.raise_for_status()
        response_data = resp.json()
        return TasksManagerResponse.model_validate(response_data)
    
    def get_new_iot_detected(
        self
    ) -> List:
        url = 'https://app.rideatom.com/api/v2/admin/trackers/new-iot-detector'
        headers = {"authorization": self.token}
        resp = requests.get(url, headers=headers)
        resp.raise_for_status()
        iots_data = resp.json().get('data', [])
        return iots_data
    
    def get_statistics(
        self
    ) -> Statistics:
        url = 'https://app.rideatom.com/api/v2/admin/dashboard/statistics'
        headers = {"authorization": self.token}
        resp = requests.get(url, headers=headers)
        resp.raise_for_status()
        stats_data = resp.json()
        stats_data['total_vehicles'] = (
    stats_data['available_vehicles'] +
    stats_data['in_use_vehicles'] +
    stats_data['charging_vehicles'] +
    stats_data['in_service_vehicles'] +
    stats_data['discharged_vehicles'] +
    stats_data['needs_investigation_vehicles'] +
    stats_data['stolen_vehicles'] +
    stats_data['not_ready_vehicles'] +
    stats_data['transportation_vehicles'] +
    stats_data['storage_vehicles']
)
        stats_data['all_vehicles'] = (
    stats_data['available_vehicles'] +
    stats_data['in_use_vehicles'] +
    stats_data['charging_vehicles'] +
    stats_data['in_service_vehicles'] +
    stats_data['discharged_vehicles'] +
    stats_data['needs_investigation_vehicles'] +
    stats_data['stolen_vehicles'] +
    stats_data['not_ready_vehicles'] +
    stats_data['transportation_vehicles'] +
    stats_data['storage_vehicles']
)
        return Statistics.model_validate(stats_data)

    def set_task(
        self,
        task_type: tasks_types,
        priority: Literal['LOW', 'MEDIUM', 'HIGH'],
        description: str,
        vehicle_id: int
    ) -> bool:
        url = 'https://app.rideatom.com/api/v2/admin/task-manager/manage'
        headers = {"authorization": self.token}
        now = datetime.now()
        data = {
            "type_id": tasks[task_type],
            "priority": priority,
            "description": description,
            "start_date": now.strftime("%Y-%m-%d"),
            "start_time": (now + timedelta(minutes=1)).strftime("%H:%M"),
            "vehicle_id": vehicle_id
        }
        resp = requests.post(url, json=data, headers=headers)
        resp.raise_for_status()
        if resp.status_code != 200:
            return False
        return True
    
    def send_notification(
        self,
        title: str, message: str, user_id: int
    ) -> bool:
        url = 'https://app.rideatom.com/api/v2/admin/user/send-push-notification'
        headers = {"authorization": self.token}
        data = {
            "title": title,
            "message": message,
            "user_id": user_id
        }
        resp = requests.post(url, json=data, headers=headers)
        resp.raise_for_status()
        if resp.status_code != 200:
            return False
        return True

    def delete_task(self, entity_id: int) -> bool:
        url = 'https://app.rideatom.com/api/v2/admin/task-manager/review'
        headers = {"authorization": self.token}
        data = {"action": "DELETE", "entity_id": entity_id}
        resp = requests.post(url, json=data, headers=headers)
        resp.raise_for_status()
        if resp.status_code != 200:
            return False
        return True

    def done_task(self, entity_id: int) -> bool:
        url = 'https://app.rideatom.com/api/v2/admin/task-manager/review'
        headers = {"authorization": self.token}
        data = {"action": "DONE", "entity_id": entity_id}
        resp = requests.post(url, json=data, headers=headers)
        resp.raise_for_status()
        if resp.status_code != 200:
            return False
        return True

    def send_command(self, command: commands, vehicle_id: int) -> bool:
        url = 'https://app.rideatom.com/api/v2/admin/vehicle/command'
        headers = {"authorization": self.token}
        data = {"command": command, "vehicle_id": vehicle_id}
        resp = requests.post(url, json=data, headers=headers)
        resp.raise_for_status()
        if resp.status_code != 200:
            return False
        return True

    def set_status(
        self,
        status: Literal['READY', 'DISCHARGED', 'CHARGING', 'NEED_INVESTIGATION', 'NEED_SERVICE',
                       'TRANSPORTATION', 'STORAGE', 'NOT_READY', 'STOLEN', 'DEPRECATED'],
        vehicle_id: int
    ) -> bool:
        url = 'https://app.rideatom.com/api/v2/admin/vehicle/status'
        headers = {"authorization": self.token}
        data = {"status": status, "vehicle_id": vehicle_id}
        resp = requests.put(url, json=data, headers=headers)
        resp.raise_for_status()
        if resp.status_code != 200:
            return False
        return True

    def get_vehicle_activity(self, vehicle_id:int) -> List[VehicleActivity]:
        url = 'https://app.rideatom.com/api/v2/admin/vehicles/activity'
        headers = {"authorization": self.token}
        data = {"vehicle_id": vehicle_id}
        resp = requests.post(url, json=data, headers=headers)
        resp.raise_for_status()
        activity_data = resp.json()
        if isinstance(activity_data, dict):
            activity_data = activity_data.get('data', [])
        return [VehicleActivity.model_validate(item) for item in activity_data]

print("-----------------------")
print("ATOM Mobility API | R12")
print("     t.me/mc_c0rp      ")
print("       started!        ")
print("-----------------------")