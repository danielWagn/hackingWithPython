from fitness import app, db
from flask import render_template, request, flash, url_for, redirect
from sqlalchemy import text


@app.route('/')
def home_page():
    cookie = request.cookies.get('name')
    print(cookie)
    return render_template('home.html', cookie=cookie)


@app.route('/login', methods=['GET', 'POST'])
def login_page():


    print("login was called")

    if request.method == 'POST':
        username = request.form.get('Username')
        password = request.form.get('Password')
        print("Here you can hack me with: " + username + " " + password)

        if username is None or isinstance(username, str) is False or len(username) < 3:
            print("not valid")
            flash(f"Username is not valid", category='warning')
            return render_template('login.html', cookie=None)

        if password is None or isinstance(password, str) is False or len(password) < 3:
            print("something with oasswort")
            flash(f"Password is not valid", category='warning')
            return render_template('login.html', cookie=None)

        query_stmt = f"select username from athletes where username = '{username}' and password = '{password}'"
        print(query_stmt)

        result = db.session.execute(text(query_stmt))

        user = result.fetchall()

        if not user:
            print("User error")
            flash(f"Try Again", category='warning')
            return render_template('login.html', cookie=None)

        flash(f"'{user}', logged in", category='success')
        print(user)

        resp = redirect(url_for('exercise_page'))
        resp.set_cookie('name', username)
        return resp



    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register_page():

    print("register was called")

    if request.method == 'POST':
        username = request.form.get('Username')
        email = request.form.get('Email')
        password = request.form.get('Password')
        password_confirm = request.form.get('Password_Confirm')


        if username is None or isinstance(username, str) is False or len(username) < 3:
            print("not valid")
            flash(f"Username is not valid", category='warning')
            return render_template('register.html', cookie=None)

        if email is None or isinstance(email, str) is False or len(email) < 3:
            print("not valid")
            flash(f"Email is not valid", category='warning')
            return render_template('register.html', cookie=None)

        if password is None or isinstance(password, str) is False or len(password) < 3:
            print("something with oasswort")
            flash(f"Password is not valid", category='warning')
            return render_template('register.html', cookie=None)

        if password_confirm != password:
            flash(f"Password not the same", category='warning')
            return render_template('register.html', cookie=None)


        query_stmt = f"select username from athletes where username = '{username}'"
        print(query_stmt)

        result = db.session.execute(text(query_stmt))
        user = result.fetchone()

        if user:
            flash(f"Username is already existing")
            return redirect(url_for('register_page'), cookie=None)

        query_insert = f"insert into athletes (username, email_address, password) VALUES ('{username}', '{email}', '{password}')"
        db.session.execute(text(query_insert))
        db.session.commit()

        flash(f"User registered", category='success')

        resp = redirect(url_for('exercise_page'))
        resp.set_cookie('name', username)
        return resp

    return render_template('register.html')


@app.route('/exercises')
def exercise_page():

    cookie = request.cookies.get('name')
    print(cookie)

    if not request.cookies.get('name'):
        print('no cookie')
        return redirect(url_for('login_page'))

    query_stmt = f"select * from exercise"
    result = db.session.execute(text(query_stmt))
    itemsquery = result.fetchall()

    print(itemsquery)

    return render_template('exercises.html', items=itemsquery, cookie=cookie)


@app.route('/logout')
def logout():
    resp = redirect(url_for('home_page'))
    resp.set_cookie('name', value='', expires=0)
    return resp


@app.route('/new_exercise', methods=['GET', 'POST'])
def new_exercise():
    cookie = request.cookies.get('name')
    print(cookie)
    if not cookie:
        print("no cookie")
        return redirect(url_for('login_page'))

    if request.method == 'POST':
        intensity = request.form.get('Intensity')
        username = request.form.get('Username')
        title = request.form.get('Title')
        description = request.form.get('Description')

        query_insert = f"insert into exercise (intensity, username, title, description) values ('{intensity}', '{username}', '{title}', '{description}')"
        db.session.execute(text(query_insert))
        db.session.commit()
        resp = redirect(url_for('exercise_page'))
        resp.set_cookie('name', cookie)
        return resp

    return render_template('new_exercise.html', cookie=cookie)

@app.route('/exercise/<int:item_id>', methods=['GET'])
def exercise(item_id):
    query_stmt = f"select * from exercise where id={item_id}"
    result = db.session.execute(text(query_stmt))
    item = result.fetchone()
    if not item:
        print("No such item")
        # error handling

    cookie = request.cookies.get('name')

    return render_template('select_exercise.html', items=item, cookie=cookie)
