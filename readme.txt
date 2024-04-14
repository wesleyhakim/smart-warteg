Used libraries
asgiref==3.7.2
Django==4.2.7
joblib==1.3.2
numpy==1.26.2
paho-mqtt==1.6.1
pandas==2.1.3
python-dateutil==2.8.2
pytz==2023.3.post1
scikit-learn==1.3.1
scipy==1.11.4
six==1.16.0
sqlparse==0.4.4
threadpoolctl==3.2.0
tzdata==2023.3

To run this website dashboard, upload the NodeRED file named node_red.json to NodeRED and then deploy the flow. It is recommended to run the framework in a python environment. Install all libraries required which can be found above this text or in requirements.txt file. Run "py manage.py runserver" in command prompt using an environment. Type localhost:8000 in your browser to open the webpage once the server is running. You could also run the server in other ports using "py manage.py runserver 0.0.0.0:<any port number>". Both NodeRED flow and web server need to be running for the webpage to run perfectly.
