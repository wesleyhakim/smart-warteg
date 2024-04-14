from django.shortcuts import render
from django.utils import timezone
import numpy as np
import random
from django.http import JsonResponse

from .models import DishCleanerActuator
from .models import DishCleanerSensor

from .models import StoveSafetyActuator
from .models import StoveSafetySensor

from .models import CustomerActuator
from .models import CustomerSensor


from django.http import JsonResponse
from urllib.parse import unquote
from django.http import JsonResponse

from django.http import JsonResponse
from urllib.parse import unquote
import joblib
import os
from django.conf import settings
import paho.mqtt.client as mqtt
import pandas as pd


# # Global variables for storing the most recent sensor data
recent_sensor_data = None
sensor_data_lock = None  # No need for threading.Lock()

# MQTT Broker Settings
broker_address = "127.0.0.1"
port = 1883
'dish/sensor/dish_level_detector'
sensor_data = [
    {"name": "Dish level detector",
        "topic": 'dish/sensor/dish_level_detector', "class": DishCleanerSensor},
    {"name": "Waterflow monitor", "topic": 'dish/sensor/waterflow_monitor',
        "class": DishCleanerSensor},
    {"name": "Dish weight reader", "topic": 'dish/sensor/dish_weight_reader',
        "class": DishCleanerSensor},
    {"name": "Temperature reader", "topic": 'stove/sensor/temperature_reader',
        "class": StoveSafetySensor},
    {"name": "Gas leak detector", "topic": 'stove/sensor/gas_leak_detector',
        "class": StoveSafetySensor},
    {"name": "Smoke detector", "topic": 'stove/sensor/smoke_detector',
        "class": StoveSafetySensor},
    {"name": "Camera", "topic": 'customer/sensor/camera', "class": CustomerSensor},
    {"name": "Motion detector", "topic": 'customer/sensor/motion_detector',
        "class": CustomerSensor},
    {"name": "Sound sensor", "topic": 'customer/sensor/sound_sensor',
        "class": CustomerSensor},
]

# Callback when the client receives a CONNACK response from the server


def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")

    # Subscribe to all topics in sensor_data
    for data in sensor_data:
        client.subscribe(data["topic"])

# Callback when a message is received from the server


def on_message(client, userdata, msg):
    global recent_sensor_data

    try:
        payload = msg.payload.decode("utf-8")
        #print(f"Received payload: {payload}")

        # Extract the corresponding data entry
        data_entry = next(
            entry for entry in sensor_data if entry["topic"] == msg.topic)

        # Create a new SensorData instance
        recent_sensor_data = data_entry["class"].objects.create(
            name=data_entry["name"], value=payload, timestamp=timezone.now())
        # recent_sensor_data.save()

        #print(f"{data_entry['name']} data saved: {payload}")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: __ {e}\n")
        print(temperature_str)
    except KeyError as e:
        print(f"KeyError: {e}")


# Set up the MQTT client
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# Connect to the broker
client.connect(broker_address, port, 60)

# Start the client loop in the background
client.loop_start()


def show_warteg():

    dish_sensor_newest_data = {}
    for data in DishCleanerSensor.objects.values('name').distinct():
        latest_sensor = DishCleanerSensor.objects.filter(
            name=data['name']).latest('timestamp')
        dish_sensor_newest_data[data['name']] = latest_sensor

    stove_sensor_newest_data = {}
    for data in StoveSafetySensor.objects.values('name').distinct():
        latest_sensor = StoveSafetySensor.objects.filter(
            name=data['name']).latest('timestamp')
        stove_sensor_newest_data[data['name']] = latest_sensor

    customer_sensor_newest_data = {}
    for data in CustomerSensor.objects.values('name').distinct():
        latest_sensor = CustomerSensor.objects.filter(
            name=data['name']).latest('timestamp')
        customer_sensor_newest_data[data['name']] = latest_sensor
    # Define model paths
    dish_rotator_model_path = os.path.join(
        settings.BASE_DIR, 'smartWarteg', 'ML', 'dish_cleaner_rotator.joblib')
    dish_valve_model_path = os.path.join(
        settings.BASE_DIR, 'smartWarteg', 'ML', 'sink_water_valve.joblib')
    dish_soap_model_path = os.path.join(
        settings.BASE_DIR, 'smartWarteg', 'ML', 'dish_soap_pump.joblib')

    water_sprinkler_model_path = os.path.join(
        settings.BASE_DIR, 'smartWarteg', 'ML', 'water_sprinkler_model.joblib')
    fire_alarm_model_path = os.path.join(
        settings.BASE_DIR, 'smartWarteg', 'ML', 'fire_alarm_model.joblib')
    gas_exhaust_model_path = os.path.join(
        settings.BASE_DIR, 'smartWarteg', 'ML', 'gas_exhaust_model.joblib')

    sound_alert_model_path = os.path.join(
        settings.BASE_DIR, 'smartWarteg', 'ML', 'sound_alert_model.joblib')
    light_model_path = os.path.join(
        settings.BASE_DIR, 'smartWarteg', 'ML', 'light_model.joblib')
    monitor_model_path = os.path.join(
        settings.BASE_DIR, 'smartWarteg', 'ML', 'monitor_model.joblib')

    # Load models
    dish_rotator_model = joblib.load(dish_rotator_model_path)
    dish_soap_model = joblib.load(dish_soap_model_path)
    dish_valve_model = joblib.load(dish_valve_model_path)

    water_sprinkler_model = joblib.load(water_sprinkler_model_path)
    gas_exhaust_model = joblib.load(gas_exhaust_model_path)
    fire_alarm_model = joblib.load(fire_alarm_model_path)

    sound_alert_model = joblib.load(sound_alert_model_path)
    light_model = joblib.load(light_model_path)
    monitor_model = joblib.load(monitor_model_path)

    # Predict using the models
    dish_sensor_newest_data_array = pd.DataFrame(
        np.array([float(i.value)
                 for i in dish_sensor_newest_data.values()]).reshape(1, -1),
        columns=['dish_level_detector',
                 'waterflow_monitor', 'dish_weight_reader']
    )

    stove_sensor_newest_data_array = pd.DataFrame(
        np.array([float(i.value)
                 for i in stove_sensor_newest_data.values()]).reshape(1, -1),
        columns=['temperature_reader', 'gas_leak_detector', 'smoke_detector']
    )

    customer_sensor_newest_data_array = pd.DataFrame(
        np.array([float(i.value)
                 for i in customer_sensor_newest_data.values()]).reshape(1, -1),
        columns=['camera', 'motion_detector', 'sound_sensor']
    )
    dish_rotator_prediction = dish_rotator_model.predict(
        dish_sensor_newest_data_array)[0]
    dish_soap_prediction = dish_soap_model.predict(
        dish_sensor_newest_data_array)[0]
    dish_valve_prediction = dish_valve_model.predict(
        dish_sensor_newest_data_array)[0]

    stove_sprinkler_prediction = water_sprinkler_model.predict(
        stove_sensor_newest_data_array)[0]
    stove_gas_prediction = gas_exhaust_model.predict(
        stove_sensor_newest_data_array)[0]
    stove_fire_prediction = fire_alarm_model.predict(
        stove_sensor_newest_data_array)[0]

    client.publish("fire", stove_fire_prediction)

    customer_alert_prediction = sound_alert_model.predict(
        customer_sensor_newest_data_array)[0]
    customer_light_prediction = light_model.predict(
        customer_sensor_newest_data_array)[0]
    customer_monitor_prediction = monitor_model.predict(
        customer_sensor_newest_data_array)[0]

    value = [dish_rotator_prediction, dish_valve_prediction, dish_soap_prediction,
             stove_sprinkler_prediction, stove_fire_prediction, stove_gas_prediction,
             customer_alert_prediction, customer_light_prediction, customer_monitor_prediction
             ]
    actuator_data = [
        {"name": "Dish cleaner rotator", "class": DishCleanerActuator,
            "subsystem": "dish cleaning", "min": 0, "max": 10, "step": 1},
        {"name": "Sink water valve", "class": DishCleanerActuator,
            "subsystem": "dish cleaning", "threshold": 8},
        {"name": "Dish soap pump", "class": DishCleanerActuator,
            "subsystem": "dish cleaning", "min": 0, "max": 5, "step": 1},

        {"name": "Water sprinkler", "class": StoveSafetyActuator,
            "subsystem": "stove safety", "min": 0, "max": 100, "step": 1},
        {"name": "Fire alarm", "class": StoveSafetyActuator,
            "subsystem": "stove safety", "threshold": 8},
        {"name": "Gas exhaust", "class": StoveSafetyActuator,
            "subsystem": "stove safety", "min": 0, "max": 100, "step": 1},

        {"name": "Sound alert", "class": CustomerActuator,
            "subsystem": "customer", "min": 0, "max": 2, "step": 1},
        {"name": "Light", "class": CustomerActuator,
            "subsystem": "customer", "threshold": 8},
        {"name": "Monitor", "class": CustomerActuator,
            "subsystem": "customer", "min": 0, "max": 10, "step": 1},
    ]

    i = 0
    for data in actuator_data:
        data['class'].objects.create(
            name=data['name'], status=value[i], timestamp=timezone.now())
        i += 1
    i = 0

    dish_actuator_newest_data = {}
    for data in DishCleanerActuator.objects.values('name').distinct():
        latest_actuator = DishCleanerActuator.objects.filter(
            name=data['name']).latest('timestamp')
        dish_actuator_newest_data[data['name']] = latest_actuator

    stove_actuator_newest_data = {}
    for data in StoveSafetyActuator.objects.values('name').distinct():
        latest_actuator = StoveSafetyActuator.objects.filter(
            name=data['name']).latest('timestamp')
        stove_actuator_newest_data[data['name']] = latest_actuator

    customer_actuator_newest_data = {}

    for data in CustomerActuator.objects.values('name').distinct():

        latest_actuator = CustomerActuator.objects.filter(
            name=data['name']).latest('timestamp')
        customer_actuator_newest_data[data['name']] = latest_actuator

    customer_actuator_js = []
    for i in customer_actuator_newest_data.values():
        customer_actuator_js.append(float(i.status))

    dish_actuator_js = []
    for i in dish_actuator_newest_data.values():
        dish_actuator_js.append(float(i.status))

    stove_actuator_js = []
    for i in stove_actuator_newest_data.values():
        stove_actuator_js.append(float(i.status))
    return {'dish_sensor': dish_sensor_newest_data.values(),
            'dish_actuator': list(dish_actuator_newest_data.values()),
            'stove_sensor': stove_sensor_newest_data.values(),
            'stove_actuator': list(stove_actuator_newest_data.values()),
            'customer_sensor': customer_sensor_newest_data.values(),
            'customer_actuator': list(customer_actuator_newest_data.values()),
            'customer_actuator_js': customer_actuator_js,
            'stove_actuator_js': stove_actuator_js,
            'dish_actuator_js': dish_actuator_js}


def get_recent_sensor_data(request, sensor_name, database):
    # Determine the model based on the sensor_name
    sensor = unquote(sensor_name)
    if database == "dish":
        model_class = DishCleanerSensor
    elif database == "stove":
        model_class = StoveSafetySensor
    elif database == "customer":
        model_class = CustomerSensor
    else:
        # Handle other sensor types or raise an error
        return JsonResponse({'error': 'Invalid sensor type'})

    # Query the database to get the 100 most recent sensor data
    recent_sensor_data = model_class.objects.filter(
        name=sensor).order_by('-timestamp')[:100]

    # Serialize the data to JSON format
    serialized_data = [
        {'timestamp': data.timestamp.timestamp(), 'value': float(data.value)}
        for data in recent_sensor_data
    ]

    return JsonResponse({'sensor_data': serialized_data})


def get_recent_actuator_data(request, actuator_name, database):
    # Determine the model based on the sensor_name
    actuator = unquote(actuator_name)
    if database == "dish":
        model_class = DishCleanerActuator
    elif database == "stove":
        model_class = StoveSafetyActuator
    elif database == "customer":
        model_class = CustomerActuator
    else:
        # Handle other sensor types or raise an error
        return JsonResponse({'error': 'Invalid sensor type'})

    # Query the database to get the 100 most recent sensor data
    recent_actuator_data = model_class.objects.filter(
        name=actuator).order_by('-timestamp')[:100]

    # Serialize the data to JSON format
    serialized_data = [
        {'timestamp': data.timestamp.timestamp(), 'value': float(data.status)}
        for data in recent_actuator_data
    ]

    return JsonResponse({'actuator_data': serialized_data})


def show_overview(request):
    data = show_warteg()
    return render(request, 'smartWarteg/overview.html', data)


def show_element(request, id):
    data = show_warteg()
    alamat = id[3:]
    return render(request, 'smartWarteg/element/{}.html'.format(alamat), data)
# def update_live(request):
#     data = show_warteg()


def show_dish(request):
    data = show_warteg()
    return render(request, 'smartWarteg/dish.html', data)


def show_stove(request):
    data = show_warteg()
    return render(request, 'smartWarteg/stove.html', data)


def show_customer(request):
    data = show_warteg()
    return render(request, 'smartWarteg/customer.html', data)


def show_penjelasan(request):
    data = show_warteg()
    return render(request, 'smartWarteg/penjelasan.html', data)

def show_dish_history(request):
    data = show_warteg()
    return render(request, 'smartWarteg/dishHistory.html', data)

def show_stove_history(request):
    data = show_warteg()
    return render(request, 'smartWarteg/stoveHistory.html', data)

def show_customer_history(request):
    data = show_warteg()
    return render(request, 'smartWarteg/customerHistory.html', data)
