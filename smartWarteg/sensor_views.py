from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import DishCleanerSensor, StoveSafetySensor, CustomerSensor


def get_recent_sensor_data(request, sensor_name):
    # Determine the model based on the sensor_name
    if sensor_name.startswith("dish_"):
        model_class = DishCleanerSensor
    elif sensor_name.startswith("stove_"):
        model_class = StoveSafetySensor
    elif sensor_name.startswith("customer_"):
        model_class = CustomerSensor
    else:
        # Handle other sensor types or raise an error
        return JsonResponse({'error': 'Invalid sensor type'})

    # Query the database to get the 100 most recent sensor data
    recent_sensor_data = model_class.objects.filter(
        name=sensor_name).order_by('-timestamp')[:100]

    # Serialize the data to JSON format
    serialized_data = [
        {'timestamp': data.timestamp.timestamp(), 'value': float(data.value)}
        for data in recent_sensor_data
    ]

    return JsonResponse({'sensor_data': serialized_data})
