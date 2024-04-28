from flask import Flask, render_template
import mysql.connector

app = Flask(__name__)
app.config['SECRET_KEY'] = 'akfbibibibfkwiw'

# Establishes local connection with database
connection = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    passwd="1236",
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

@app.route('/customer')
def customer():
    # cursor = connection.cursor()
    cursor.execute("SELECT * FROM users")
    customer = cursor.fetchall()
    return render_template('customer.html', customer=customer)

@app.route('/view')
def view():
    return 'Views will be displayed here'

if __name__ == '__main__':
    app.run()
    