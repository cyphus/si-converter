#!/usr/bin/env python3
from flask import Flask, request

app = Flask(__name__)

@app.route('/units/si')
def hello():
    request.args.get('units', '')
