# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

# Import core packages
import os

# Import Flask 
from flask import Flask
import pymysql


# Inject Flask magic
app = Flask(__name__)

app.secret_key = "dfuio0-9876rghikl987"


dbConn = pymysql.connect(
    host='pamplin-bit2020.mysql.database.azure.com',
    port=3306,
    user='bit4444group11',
    password='g4iDIjVsjAhmGJmW',
    database='bit4444group11',
    ssl={
        'ca':'DigiCertGlobalRootCA.crt.pem' 
    },
    cursorclass=pymysql.cursors.DictCursor
)

cursor = dbConn.cursor()

from app import views

