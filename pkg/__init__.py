"""Import flask"""

from flask import Flask
"""To import sqlalchemy"""

from flask_sqlalchemy import SQLAlchemy

from flask_wtf.csrf import CSRFProtect
from flask_mail import Mail


"""Instantiate Flask Object"""

app = Flask(__name__,instance_relative_config=True)

app.config.from_pyfile('config.py')

db=SQLAlchemy(app)
csrf = CSRFProtect(app)
mail=Mail(app)

"""Importing routes"""
from pkg import mymodels
from pkg.myroutes import user_route



