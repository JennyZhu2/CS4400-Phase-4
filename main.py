from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector

app = Flask(__name__)
app.config['SECRET_KEY'] = 'akfbibibibfkwiw'

# Establishes local connection with database
connection = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
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
# cursor.callproc('remove_customer', ("vding123"))
# cursor.execute("SELECT * FROM customers")


# for x in cursor:
#      print(x)

# @app.route('/', methods=['POST', 'GET'])
# def home():
#     return redirect(url_for('customer'))

@app.route('/customer', methods=['POST', 'GET'])
def addCustomer():
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM customers")
    customer = cursor.fetchall()
    if request.method == "POST":
        # fetch data from form inputs
        uname = request.form['uname']
        fname = request.form['fname']
        lname = request.form['lname']
        address = request.form['address']
        bdate = request.form['bdate']
        rating = request.form['rating']
        credit = request.form['credit']
        try:
            # call mysql stored procedure and commit changes
            cursor.callproc('add_customer', (uname, fname, lname, address, bdate, rating, credit))
            connection.commit()
            cursor.close()
            return redirect('/customer')
        except Exception as e:
            flash(f'Cannot add customer: {e}')
    cursor.close()
    # populate webpage with queried entries
    return render_template('customer.html', customer=customer)

@app.route('/remove_customer', methods=['POST', 'GET'])
def removeCustomer():
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM customers")
    customer = cursor.fetchall()
    if request.method == "POST":
        uname = request.form['uname']
        try:
            cursor.callproc('remove_customer', [uname])
            connection.commit()
            cursor.close()
            return redirect('/customer')
        except Exception as e:
            flash(f'Cannot delete customer: {e}')
    cursor.close()
    return render_template('customer.html', customer=customer)

@app.route('/customer_credits', methods=['POST', 'GET'])
def customerCredits():
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM customers")
    customer = cursor.fetchall()
    if request.method == "POST":
        uname = request.form['uname']
        money = request.form['money']
        try:
            cursor.callproc('increase_customer_credits', [uname, money])
            connection.commit()
            cursor.close()
            return redirect('/customer')
        except Exception as e:
            flash(f'Cannot delete customer: {e}')
    cursor.close()
    return render_template('customer.html', customer=customer)
    
@app.route('/drone_pilot', methods=['POST', 'GET'])
def drone_pilot():
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM drone_pilots")
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
        try:
            # call mysql stored procedure and commit changes
            cursor.callproc('add_drone_pilot',
                            (uname, first_name, last_name, address, birthdate, taxID, service, salary, licenseID,
                             experience))
            connection.commit()
            cursor.close()
            return redirect('/drone_pilot')
        except Exception as e:
            flash(f'Cannot add drone pilot: {e}')

    cursor.close()
    return render_template('add_drone_pilot.html', drone_pilots=drone_pilots)

@app.route('/delete_pilot', methods=['GET', 'POST'])
def delete_pilot():
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
        return redirect('/drone_pilot')  # Stay on the same page after removing
    cursor.close()
    return render_template('drone_pilot.html', drone_pilots=drone_pilots)

@app.route('/product', methods=['POST', 'GET'])
def addProduct():
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM products")
    product = cursor.fetchall()
    if request.method == "POST":
        # fetch data from form inputs
        barcode = request.form['barcode']
        pname = request.form['pname']
        weight = request.form['weight']
        try:
            # call mysql stored procedure and commit changes
            cursor.callproc('add_product', (barcode, pname, weight))
            connection.commit()
            cursor.close()
            return redirect('/product')
        except Exception as e:
            flash(f'Cannot add product: {e}')
    cursor.close()
    # populate webpage with queried entries
    return render_template('product.html', product=product)

@app.route('/remove_product', methods=['POST', 'GET'])
def removeProduct():
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM products")
    product = cursor.fetchall()
    if request.method == "POST":
        barcode = request.form['barcode']
        try:
            cursor.callproc('remove_product', [barcode])
            connection.commit()
            cursor.close()
            return redirect('/product')
        except Exception as e:
            flash(f'Cannot delete product: {e}')
    cursor.close()
    return render_template('product.html', product=product)

@app.route('/drone', methods=['POST', 'GET'])
def addDrone():
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM drones")
    drone = cursor.fetchall()
    cursor.execute("SELECT * FROM drone_pilots")
    drone_pilots = cursor.fetchall()
    if request.method == "POST":
        # fetch data from form inputs
        storeid = request.form['storeid']
        dronetag = request.form['dronetag']
        capacity = request.form['capacity']
        pilot = request.form['pilot']
        remtrips = request.form['remtrips']
        try:
            # call mysql stored procedure and commit changes
            cursor.callproc('add_drone', (storeid, dronetag, capacity, remtrips, pilot))
            connection.commit()
            cursor.close()
            return redirect('/drone')
        except Exception as e:
            flash(f'Cannot add drone: {e}')
    cursor.close()
    # populate webpage with queried entries
    return render_template('drone.html', drone=drone, drone_pilots=drone_pilots)

@app.route('/remove_drone', methods=['POST', 'GET'])
def removeDrone():
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM drones")
    drone = cursor.fetchall()
    cursor.execute("SELECT * FROM drone_pilots")
    drone_pilots = cursor.fetchall()
    if request.method == "POST":
        storeid = request.form['storeid']
        dronetag = request.form['dronetag']
        try:
            cursor.callproc('remove_drone', [storeid, dronetag])
            connection.commit()
            cursor.close()
            return redirect('/drone')
        except Exception as e:
            flash(f'Cannot delete drone: {e}')
    cursor.close()
    return render_template('drone.html', drone=drone, drone_pilots=drone_pilots)

@app.route('/refuel_drone', methods=['POST', 'GET'])
def refuelDrone():
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM drones")
    drone = cursor.fetchall()
    cursor.execute("SELECT * FROM drone_pilots")
    drone_pilots = cursor.fetchall()
    if request.method == "POST":
        storeid = request.form['storeid']
        dronetag = request.form['dronetag']
        refueledtrips = request.form['refueledtrips']
        try:
            cursor.callproc('repair_refuel_drone', [storeid, dronetag, refueledtrips])
            connection.commit()
            cursor.close()
            return redirect('/drone')
        except Exception as e:
            flash(f'Cannot refuel drone: {e}')
    cursor.close()
    return render_template('drone.html', drone=drone, drone_pilots=drone_pilots)

@app.route('/swap_drone', methods=['POST', 'GET'])
def swapDrone():
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM drones")
    drone = cursor.fetchall()
    cursor.execute("SELECT * FROM drone_pilots")
    drone_pilots = cursor.fetchall()
    print(drone_pilots)
    if request.method == "POST":
        incoming = request.form['incoming']
        outgoing = request.form['outgoing']
        try:
            cursor.callproc('swap_drone_control', [incoming, outgoing])
            connection.commit()
            cursor.close()
            return redirect('/drone')
        except Exception as e:
            flash(f'Cannot swap: {e}')
    cursor.close()
    return render_template('drone.html', drone=drone, drone_pilots=drone_pilots)

@app.route('/view')
def view():
    return 'Views will be displayed here'

@app.route('/order')
def order():
    return 'Orders will be displayed here'

@app.route('/')
def main():
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)
    