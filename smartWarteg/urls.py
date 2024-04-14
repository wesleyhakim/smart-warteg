from django.urls import path, include
from . import views
from .views import get_recent_sensor_data, get_recent_actuator_data

app_name = 'smartWarteg'

urlpatterns = [
    path('', views.show_overview, name='overview'),
    path('overview/', views.show_overview, name='overview'),
    path('dish/', views.show_dish, name='dish'),
    path('stove/', views.show_stove, name='stove'),
    path('customer/', views.show_customer, name='customer'),
    path('penjelasan/', views.show_penjelasan, name='penjelasan'),
    path('get_recent_sensor_data/<sensor_name>/<database>/',
         get_recent_sensor_data, name='get_recent_sensor_data'),
    path('get_recent_actuator_data/<actuator_name>/<database>/',
         get_recent_actuator_data, name='get_recent_actuator_data'),
    path('show_element/<str:id>/', views.show_element, name='show_element'),
    path('dish/history/', views.show_dish_history, name='dish_history'),
    path('stove/history/', views.show_stove_history, name='stove_history'),
    path('customer/history/', views.show_customer_history, name='customer_history'),
]
