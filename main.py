from flask import Flask, render_template, request, redirect, url_for, flash
from flaskext.mysql import MySQL


app = Flask(__name__)
app.secret_key = 'many random bytes'

app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'crud'

mysql = MySQL(app)


@app.route('/')
def Index():
    db = mysql.get_db().cursor()
    db.execute("SELECT  * FROM students")
    data = db.fetchall()
    db.close()

    return render_template('index2.html', students=data)


@app.route('/insert', methods=['POST'])
def insert():

    if request.method == "POST":
        flash("Data Inserted Successfully")
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        db =  mysql.get_db().cursor()
        db.execute(
            "INSERT INTO students (name, email, phone) VALUES (%s, %s, %s)", (name, email, phone))
        mysql.get_db().commit()
        return redirect(url_for('Index'))


@app.route('/delete/<string:id_data>', methods=['GET'])
def delete(id_data):
    flash("Record Has Been Deleted Successfully")
    cur =  mysql.get_db().cursor()
    cur.execute("DELETE FROM students WHERE id=%s", (id_data,))
    mysql.get_db().commit()
    return redirect(url_for('Index'))


@app.route('/update', methods=['POST', 'GET'])
def update():

    if request.method == 'POST':
        id_data = request.form['id']
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        cur = mysql.get_db().cursor()
        cur.execute("""
               UPDATE students
               SET name=%s, email=%s, phone=%s
               WHERE id=%s
            """, (name, email, phone, id_data))
        flash("Data Updated Successfully")
        mysql.get_db().commit()
        return redirect(url_for('Index'))


if __name__ == "__main__":
    app.run(debug=True)
