from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector

app = Flask(__name__)
app.config['SECRET_KEY'] = 'akfbibibibfkwiw'

# Establishes local connection with database
connection = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    passwd="Ameya2002",
    database="drone_dispatch",
    port = 3306
)

# cursor object interacts with database
cursor = connection.cursor()
cursor = connection.cursor(buffered=True)
#cursor.execute("INSERT INTO users (uname, first_name, last_name, address, birthdate) VALUES (%s,%s,%s,%s,%s)", ("Mary143", "Mary", "Joe", "San Diego", "1973-03-07"))
connection.commit()

# cursor.callproc('add_customer', ("Jenn482","Jenny","ZHU","Atlanta","2004-07-10","5","10"))
# cursor.execute("DESCRIBE users")
# cursor.execute("SELECT * FROM users")

# for x in cursor:
#     print(x)

@app.route('/')
def home():
    return redirect(url_for('customer')) 

@app.route('/customer', methods=['POST', 'GET'])
def customer():
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM customers")
    customer = cursor.fetchall()
    if request.method == "POST":
        uname = request.form['uname']
        fname = request.form['fname']
        lname = request.form['lname']
        address = request.form['address']
        bdate = request.form['bdate']
        rating = request.form['rating']
        credit = request.form['credit']
        cursor.callproc('add_customer', (uname, fname, lname, address, bdate, rating, credit))
        connection.commit()
    cursor.close()
    return render_template('customer.html', customer=customer)
    
@app.route('/drone_pilot', methods=['POST', 'GET'])
def drone_pilot():
    cursor = connection.cursor()
    cursor.execute("SELECT uname, licenseID, experience FROM drone_pilots")
    drone_pilots = cursor.fetchall()
    if request.method == "POST":
        uname = request.form['uname']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        address = request.form['address']
        birthdate = request.form['birthdate']
        taxID = request.form['taxID']
        service = request.form['service']
        salary = request.form['salary']
        licenseID = request.form['licenseID']
        experience = request.form['experience']
        cursor.callproc('add_drone_pilot', [uname, first_name, last_name, address, birthdate, taxID, service, salary, licenseID, experience])
        connection.commit()
    cursor.close()
    return render_template('add_drone_pilot.html', drone_pilots=drone_pilots)

@app.route('/delete_drone_pilot', methods=['GET', 'POST'])
def delete_drone_pilot():
    cursor = connection.cursor()
    cursor.execute("SELECT uname FROM drone_pilots")
    drone_pilots = cursor.fetchall()

    if request.method == 'POST':
        uname = request.form.get('uname')
        try:
            cursor.callproc('remove_drone_pilot', [uname])
            connection.commit()
        except Exception as e:
            flash(f'An error occurred: {e}')
        finally:
            cursor.close()
        return redirect(url_for('delete_drone_pilot'))  # Stay on the same page after removing

    cursor.close()
    return render_template('delete_drone_pilot.html', drone_pilots=drone_pilots)
@app.route('/view')
def view():
    return 'Views will be displayed here'

if __name__ == '__main__':
    app.run()
    