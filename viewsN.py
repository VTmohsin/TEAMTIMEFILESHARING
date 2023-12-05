from flask import Flask, render_template, request, redirect, json, jsonify, session, flash
from app import app, dbConn, cursor


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/visualization')
def visualization():
     sql = "select count(username) from acctcreation"
     cursor.execute(sql)
     result = cursor.fetchall()
     chartData = json.dumps(result)
     return render_template('viz.html', chartData = chartData)

@app.route('/login', methods=['GET', 'POST'])  #UP TO DATE
def login():
    if request.method == 'POST':
        data = request.json
        #get user input values from the form
        email = request.form.get("mail")
        password = request.form.get("p")
        errors = []


        # Validate form entries
        if not email:
            errors.append('Email is required.')
        if not password:
            errors.append('Password is required.')
        
        if not errors:
            
                sql = "SELECT user_pass FROM acctcreation WHERE email = %s"
                cursor.execute(sql, (email))
                result = cursor.fetchone()

                if errors:
                    for error in errors:
                        flash(error, 'error')

        return render_template('viz.html', pword = password, e = email)
    
    return render_template('login.html')


@app.route('/submit-form', methods=['GET', 'POST'])
def submit_form():
    if request.method == 'POST':
        # Get user input values from the form
        username = request.form.get("un")
        password = request.form.get("pw")
        fname = request.form.get("fn")
        lname = request.form.get("ln")
        email = request.form.get("em")
        phone = request.form.get("ph")
        error = False



        # Validate form entries
        if not username:
            error = True
            flash('Username is required.')
        if not password:
            error = True
            flash('Password is required.')
        if not fname:
            error = True
            flash('First name is required.')
        if not lname:
            error = True
            flash('Last name is required.')
        if not email:
            error = True
            flash('Email is required.')
        if not phone:
            error = True
            flash('Phone is required.')
        else:
            try:
                phone = int(phone)
                if phone < 1:
                    error.append('Phone number must be greater than or equal to 0.')
            except ValueError:
                error.append('Phone number must be a valid integer.')

        # Check for errors
        if error:
            return render_template('createAcct.html')

        # update database
        if not error:
            sql = "INSERT INTO acctcreation (username, user_pass, first_name, last_name, email, phone) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, [username, password, fname, lname, email, phone])
            dbConn.commit()

        flash('Account Created successfully!', 'success')
        return render_template('login.html', uname = username , pword = password, firstname = fname, lastname = lname, e = email, pnumber = phone)  # Redirect to the login page after successful account creation

    # Render form for GET request
            
    return render_template('createAcct.html') # ...(html value) = ...(var))



@app.route('/update_profile', methods=['GET','POST'])
def update_profile():
    if request.method == 'POST':
        # Check if Delete Account button was clicked
        if 'delete' in request.form:
            username = request.form.get('un')
            sql = "DELETE FROM userprofile WHERE username = %s"
            cursor.execute(sql, [username])
            dbConn.commit()

            flash('Profile deleted successfully!', 'info')
            return render_template('createAcct.html', uname = username)

        # Otherwise, proceed with profile update
        profile_pic = request.args.get("propic")
        username = request.args.get("un")
        password = request.args.get("prd")
        name = request.args.get("nm")
        gender = request.args.get("ge")
        age = request.args.get("ag")
        pronouns = request.args.get("prn")
        email = request.args.get("ema")
        bio = request.args.get("bi")
        links = request.args.get("li")

        sql = """
        UPDATE userprofile SET profile_pic = %s, username = %s, user_pass = %s, name = %s, 
                            gender = %s, age = %s, pronouns = %s, 
                            email = %s, bio = %s, links = %s
        WHERE username = %s 
        """
        cursor.execute(sql, [profile_pic, username, password, name, gender, age, pronouns, email, bio, links]) 
        dbConn.commit()

        flash('Profile updated successfully!', 'success')
        return render_template('modify.html', uname = username , pword = password, e = email, ppic = profile_pic, n = name, gen = gender, a = age, pnouns = pronouns, b = bio, l = links)

    return render_template('modify.html')
