# -*- coding: utf-8 -*-

from ishmael import app
from flask import render_template

@app.endpoint('index')
@app.route('/')
def index():
	return render_template('index.html')
