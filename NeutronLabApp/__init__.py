from flask import Flask
from celery import Celery

app = Flask(__name__)
app.config['SECRET_KEY'] = 'a-very-secret-key'
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379'

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

from NeutronLabApp import routes
from NeutronLabApp import forms



