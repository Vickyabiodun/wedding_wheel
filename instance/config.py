from flask import Flask

DEBUG=True
FLASK_ENVIRONMENT='development'
SECRET_KEY='M8PmhNk8wh+e*$!+)7LH$U'
SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root@localhost/wedding_wheel'
SQLALCHEMY_TRACK_MODIFICATIONS=False
MAIL_SERVER='smtp.gmail.com'
MAIL_PORT=465
MAIL_USERNAME='weddingwheel@gmail.com'
MAIL_PASSWORD='dbxhmlzbtdhdlhpk'
MAIL_USE_SSL=True