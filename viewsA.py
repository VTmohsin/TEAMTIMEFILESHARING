#Allie's Part

# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

# Flask modules
from flask   import render_template, request, redirect, url_for, flash, json, session, Flask, jsonify
from jinja2  import TemplateNotFound

# App modules
from app import app, dbConn, cursor
# from app.models import Profiles

# App main route + generic routing
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/newscheduletask')
def newscheduletask():
    return render_template('createnewtask.html')

#When user submits the form

@app.route('/submitnewtask', methods=['POST', 'GET'])
def SubmitNewTask():
    error = False
    esid = request.form.get("scheduleid")
    eid = request.form.get("eventid")
    responsedeadline = request.form.get("responsedeadline")
    startingdate = request.form.get("startingdate")
    endingdate = request.form.get("endingdate")

    
    if not esid:
        error = True
        flash("Please provide a Schedule ID.")   
    else:
        esid = str(esid)
        if len(esid) != 6:
            error = True
            flash("The Schedule ID should be 6 Numeric Characters.")

    if not eid:
        flash("Please provide an event ID.")
    else:
        eid = str(eid)
        if len(eid) != 6:
            error = True
            flash("The Event ID should be 6 Numeric Characters.")

    if not responsedeadline:
        error = True
        flash("Please provide a response deadline.")

    if not startingdate:
        error = True
        flash("Please provide a starting date.")

    if not endingdate:
        error = True
        flash("Please provide a ending date.")
        

    if not error:
        # update the database
        # the product id does not exist, we should add as new
        sql = "insert into eventschedule (esid, eid, startingdate, endingdate, responsedeadline) values(%s, %s, %s, %s, %s)" 
        cursor.execute(sql, [esid, eid, startingdate, endingdate, responsedeadline])
        dbConn.commit() # make the database changes permanent  
        flash("The task has been added!")   
       
        
    return render_template("createnewtask.html")
         

@app.route('/modifytask')
def modifytask():
    sql = "select esid from eventschedule"
    cursor.execute(sql)
    result = cursor.fetchall()
    return render_template('modifytask.html', eventschedule=result)

@app.route('/updatetask', methods=['POST', 'GET'])
def updateTask():
        error = False
        esid = request.form.get("esid")
        responsedeadline = request.form.get("responsedeadline")
        startingdate = request.form.get("startingdate")
        endingdate = request.form.get("endingdate")
    
        if not esid:
            error = True
            flash("Please provide a Schedule ID.")   
        if not responsedeadline:
            error = True
            flash("Please provide a response deadline.")

        if not startingdate:
            error = True
            flash("Please provide a starting date.")

        if not endingdate:
            error = True
            flash("Please provide a ending date.")

        # update the database
        if not error:
            sql = "update eventschedule set responsedeadline=%s, startingdate=%s, endingdate=%s where esid=%s"
            cursor.execute(sql, [responsedeadline, startingdate, endingdate, esid])
            dbConn.commit()
            flash("The task has been succesfully modified!")
            # sql = "select * from eventschedule where esid=%s"
            # cursor.execute(sql, [esid])
            # result = cursor.fetchall()
            return render_template("modifytask.html", esid=esid)
        return

@app.route('/searchemail')
def findavailability():
    sql = "select email from responsemanagement where availability='Yes'"
    cursor.execute(sql)
    result = cursor.fetchall()

    return render_template('availability.html', emails=result)

@app.route('/findavailability', methods=['POST','GET'])
def searchemail():

    error = False
    email = request.args.get('email')
    if not email:
        error = True
        flash("Please provide an email!")

    sql = "select * from responsemanagement where email=%s"
    cursor.execute(sql, [email])
    result = cursor.fetchall()
    print(email)


    return render_template("availabilitytable.html", emails=result)



@app.route('/findtask')
def DeleteTask():
    sql = "select esid from eventschedule"
    cursor.execute(sql)
    result = cursor.fetchall()
    return render_template('deletetask.html', eventschedule=result)


@app.route("/deletetask", methods=['POST', 'GET'])
def deletetasksubmit():
    error = False
    esid = request.form.get("esid")

    #request.args.get
    if not esid:
        error = True
        flash("Please provide a Schedule ID.")   
    
        # update the database
    if not error:
        sql = "delete from eventschedule where esid=%s"
        cursor.execute(sql, [esid])
        dbConn.commit()
        flash("The task has been succesfully deleted!")



    return render_template("deletetask.html", esid=esid)