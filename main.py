from flask import Flask, redirect, url_for, render_template, request, flash
from flask_mysqldb import MySQL


app = Flask(__name__)
app.secret_key = 'mysecretkey'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'km05010002'
app.config['MYSQL_DB'] = 'entrenamientos'
mysql = MySQL(app)


@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/adidas', methods=['POST', 'GET'])
def adidas():
    if request.method == 'POST':
        username = request.form['username']
        password = int(request.form['password'])
    
        if username != "kevin" or password != 123:
            flash("Username or password incorrect")
            return redirect(url_for('login'))

    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM ejercicios')
    data = cursor.fetchall()
            
    return render_template('mainpage.html', exercises = data)

@app.route('/registration_form', methods = ['POST'])
def form():
    if request.method == 'POST':
        name_exercise = request.form['exercise-name']
        days_exercise = request.form['exercise-days']
        week_exercise = request.form['exercise-week']
        series_exercise = request.form['exercise-series']
        reps_exercise = request.form['exercise-reps']
        duration_exercise = request.form['exercise-duration']
        
        datos = name_exercise, days_exercise, week_exercise, series_exercise, reps_exercise, duration_exercise

        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO ejercicios (NOMBRE, DIAS, SEMANA, SERIES, REPETICIONES, DURACION) VALUES (%s, %s, %s, %s, %s, %s)", datos)
        mysql.connection.commit()

        flash("¡Exercise successfully saved!")
        return redirect(url_for('adidas'))

@app.route('/edit_record/<int:id>')
def get_record(id):
    cursor = mysql.connection.cursor()
    cursor.execute(f'SELECT * FROM ejercicios WHERE ID = {id}')
    data = cursor.fetchall()

    return render_template('updateexercise.html', exercise = data[0])

@app.route('/update_record/<int:id>', methods = ['POST'])
def update_record(id):
    if request.method == 'POST':
        name_exercise = request.form['exercise-name']
        days_exercise = request.form['exercise-days']
        week_exercise = request.form['exercise-week']
        series_exercise = request.form['exercise-series']
        reps_exercise = request.form['exercise-reps']
        duration_exercise = request.form['exercise-duration']

        cursor = mysql.connection.cursor()
        cursor.execute("""
            UPDATE ejercicios
            SET NOMBRE = %s, DIAS = %s, SEMANA = %s, SERIES = %s, REPETICIONES = %s, DURACION = %s
            WHERE ID = %s
        """, (name_exercise, days_exercise, week_exercise, series_exercise, reps_exercise, duration_exercise, id))

        mysql.connection.commit()

        flash("¡Exercise succesfully updated!")
        return redirect(url_for('adidas'))

@app.route('/delete_record/<int:id>')
def delete_record(id):
    cursor = mysql.connection.cursor()
    cursor.execute(f'DELETE FROM ejercicios WHERE ID = {id}')
    mysql.connection.commit()
    
    flash("¡Exercise successfully removed!")
    return redirect(url_for('adidas'))