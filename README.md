# SoftDesk

SoftDesk is a development and collaboration software publisher. This documentation describe all endpoint of an API for an issue tracking system.

## Documentation

You can find the documentation : https://documenter.getpostman.com/view/14060645/2s8ZDYY2nL

## Installation 

Clone repository
```
git clone https://github.com/Tortique/SoftDesk.git
```

Create a new venv
```
python -m venv env
```

Activate him
```
env\scripts\activate.bat
```

Install all requirements
```
pip install -r requirements.txt
```

Make migrations and migrate
```
python manage.py makemigrations

python manage.py migrate
```

And run server
```
python manage.py runserver
```
