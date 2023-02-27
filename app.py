#!/usr/bin/python3
from flask import Flask, render_template, request
from models.driver.helper import *
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    """view for view ward result"""
    pu = get_polling_units()
    scores = None
    pu_info = None
    if request.method == 'POST':
        uniqueid = request.form['select_pu']
        if uniqueid != 'Select Polling Unit':
            uniqueid = uniqueid.split(' ')[0]
            scores = get_pu_results(uniqueid)
            pu_info = get_pu_info(uniqueid)
    return render_template('index.html',
            polling_units=pu,
            scores=scores,
            pu_info=pu_info)


@app.route('/lga/', methods=['GET', 'POST'])
def lga():
    """view for view lga result"""
    lgas = get_lgas()
    lga_result = None
    if request.method == 'POST':
        if request.form['lga_id'] != 'Select LGA':
            lga_id = request.form['lga_id']
            lga_id = lga_id.split(' ')[0]
            lga_result = get_lga_results(lga_id)
            info = get_lga_info(lga_id)
    return render_template('lga.html'
            ,lgas=lgas
            ,lga_result=lga_result
            ,info=info)


@app.route('/new/', methods=['GET', 'POST'])
def add_new_result():
    """view for add new polling unit and result"""
    if request.method == 'POST':
        args = {'polling_unit_name': request.form['pu_name']
                ,'polling_unit_number': request.form['pu_number']
                ,'polling_unit_id': request.form['pu_id']
                ,'polling_unit_description': request.form['pu_desc']
                ,'ward_id': request.form['ward'].split(' ')[0]
                ,'lga_id': request.form['lga'].split(' ')[0]
                ,'lat': request.form['lat']
                ,'long': request.form['long']
                }
        obj = {'party': request.form['party']
                ,'party_score': request.form['score']
                }
        insert_new_result(obj, **args)
        return render_template('success.html')
    lgas = get_lgas()
    wards = get_wards()
    parties   = get_parties()
    return render_template('new.html'
            ,lgas=lgas
            ,parties=parties,
            wards=wards)

