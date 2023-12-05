# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

# Flask modules
from flask   import render_template, request, redirect, url_for, flash, json
from jinja2  import TemplateNotFound

# App modules
from app import app,dbConn,cursor
# from app.models import Profiles

# App main route + generic routing
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

# Add Response

@app.route('/addResponse')
def addRes():
    return render_template('addResponse.html')

@app.route('/added', methods=['POST', 'GET'])
def addResponseSubmit():
    error = False

    # get form submitted data
    sid = request.form.get('scheduleID')
    rid = request.form.get('responseID')
    e = request.form.get('email')
    av = request.form.get('availability')
    ts = request.form.get('timeSlot')

    if not sid:
            error = True
            flash("Please provide a Schedule ID number.")
    else:
        sid = int(sid)
        if sid<0:
            error = True
            flash("The Schedule ID entered must be greater than 0.")
    
    if not rid:
            error = True
            flash("Please provide a Response ID number.")
    else:
        rid = int(rid)
        if rid<0:
            error = True
            flash("The Response ID entered must be greater than 0.")

    if not e:
            error = True
            flash("Please provide an email.")
    
    if not av:
            error = True
            flash("Please provide your availability.")

    if not ts:
            error = True
            flash("Please select a time slot.")

    #sql statements
    if not error:
        sql = "select count(*) as matchcount from responsemanagement where response_ID=%s"
        cursor.execute(sql, rid)
        result = cursor.fetchone()
        if result['matchcount'] == 0:
            sql = "insert into responsemanagement(email, schedule_ID, response_ID, availability, time_slot) values(%s, %s, %s, %s, %s)"
            cursor.execute(sql, [e, sid, rid, av, ts])
            dbConn.commit()
            flash("A new response has been added to the event.")
    
    #render the web page
    return render_template('addResponse.html', userEmail=e, schedID=sid, resID=rid, avail=av, time=ts)

# Modify Response

@app.route('/modifyResponse')
def modifyRes():
    return render_template('modifyResponse.html')

@app.route('/modified', methods=['POST', 'GET'])
def modifyResponseSubmit():
    error = False

    # get form submitted data
    sid = request.form.get('scheduleID')
    rid = request.form.get('responseID')
    e = request.form.get('email')
    av = request.form.get('availability')
    ts = request.form.get('timeSlot')

    if not sid:
            error = True
            flash("Please provide a Schedule ID number.")
    else:
        sid = int(sid)
        if sid<0:
            error = True
            flash("The Schedule ID entered must be greater than 0.")
    
    if not rid:
            error = True
            flash("Please provide a Response ID number.")
    else:
        rid = int(rid)
        if rid<0:
            error = True
            flash("The Response ID entered must be greater than 0.")

    if not e:
            error = True
            flash("Please provide an email.")
    
    if not av:
            error = True
            flash("Please provide your availability.")

    if not ts:
            error = True
            flash("Please select a time slot.")
    
    # sql statements
    sql = "update responsemanagement set email=%s, schedule_ID=%s, response_ID=%s, availability=%s, time_slot=%s where response_ID=%s"
    cursor.execute(sql, [e, sid, rid, av, ts, rid])
    dbConn.commit()
    flash("The response has been updated.")

    #render the web page
    return render_template('modifyResponse.html', userEmail=e, schedID=sid, resID=rid, avail=av, time=ts)


# Delete Response
@app.route('/deleteResponse')
def deleteRes():
    return render_template('deleteResponse.html')

@app.route('/deleted', methods=['POST', 'GET'])
def deleteResponseSubmit():
    error = False

    # get form submitted data

    rid = request.form.get('responseID')
    e = request.form.get('email')

    if not rid:
            error = True
            flash("Please provide a Response ID number.")
    else:
        rid = int(rid)
        if rid<0:
            error = True
            flash("The Response ID entered must be greater than 0.")

    if not e:
            error = True
            flash("Please provide an email.")

    # sql statements
    if not error:
        sql = "delete from responsemanagement where response_ID=%s"
        cursor.execute(sql, [rid])
        dbConn.commit()
        flash("The response has been deleted.")

    #render the web page
    return render_template('deleteResponse.html', userEmail=e, resID=rid)


# Search for  Response
@app.route('/searchResponse')
def searchRes():
    sql = "select time_slot from responsemanagement"
    cursor.execute(sql)
    result = cursor.fetchall()
    return render_template('searchResponse.html', timeSlots=result)

@app.route('/searchTable', methods=['GET'])
def Table():
    timeSlot = request.args.get('timeSlot')
    sql = "select * from responsemanagement where time_slot=%s"
    cursor.execute(sql, timeSlot)
    result = cursor.fetchall()
    print(timeSlot)

    return render_template("timeTable.html", timeSlots=result)

# Visualize Response 
@app.route('/visualizeResponse')
def visRes():
     return render_template("selectVisualize.html")

@app.route('/visualizeRes', methods=['POST', 'GET'])
def visualizeResponseSubmit():
     
     av = request.form.get('availability')

     sql = "select availability as label, schedule_id as value from responsemanagement where availability=%s"
     cursor.execute(sql,[av])
     result = cursor.fetchall()
     result = json.dumps(result)
     return render_template("visualizeResponse.html", avail=av, chartData=result)