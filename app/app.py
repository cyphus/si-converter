#!/usr/bin/env python3
from flask import Flask, request, jsonify
from . import si_convert

app = Flask(__name__)

@app.route('/units/si')
def units_si():
    unit_str = request.args.get('units', '')
    try:
        if len(unit_str) == 0:
            raise ValueError("Input unit string empty or not defined")
        response = si_convert.convert_units(unit_str)
        status = 200
    except ValueError as e:
        response = {"error": str(e)}
        status = 400
    return jsonify(response), status
