# Start app locally

export FLASK_APP=flaskr/**init**.py
export DATABASE_URL=postgressURL
flask run

https://sbb-analyse-core.herokuapp.com

#Aufbau der postgress connection url
postgres://user:password@host:port/database

#--preload ensures that only one instance of the app is running
