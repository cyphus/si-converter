#!/usr/bin/env python3
from flask import Flask, request, jsonify
from units.tokenizer import tokenize
from units.si_converter import si_convert
from units.parser import parse, coefficient

app = Flask(__name__)

@app.route('/units/si')
def units_si():
    unit_str = request.args.get('units', '')
    tokens = tokenize(unit_str)
    si_tokens = si_convert(tokens)
    rpn_tokens = parse(si_tokens)
    return jsonify({
        "unit_name": ''.join(t.text for t in si_tokens),
        # multiplication factor should have 14 significant digits
        "multiplication_factor": coefficient(rpn_tokens),
    })
