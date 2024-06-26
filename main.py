from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector

app = Flask(__name__)
app.config['SECRET_KEY'] = 'akfbibibibfkwiw'

# Establishes local connection with database
connection = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    passwd="1051",
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

@app.route('/order', methods=['POST', 'GET'])
def beginOrder():
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM order_lines")
    order_line = cursor.fetchall()
    cursor.execute("SELECT * FROM orders")
    order = cursor.fetchall()
    cursor.execute("SELECT * FROM products")
    product = cursor.fetchall()
    if request.method == "POST":
        # fetch data from form inputs
        orderid = request.form['orderid']
        soldon = request.form['soldon']
        purchasedby = request.form['purchasedby']
        store = request.form['store']
        tag = request.form['tag']
        barcode = request.form['barcode']
        price = request.form['price']
        quantity = request.form['quantity']
        try:
            # call mysql stored procedure and commit changes
            cursor.callproc('begin_order', (orderid, soldon, purchasedby, store, tag, barcode, price, quantity))
            connection.commit()
            cursor.close()
            return redirect('/order')
        except Exception as e:
            flash(f'Cannot add order: {e}')
    cursor.close()
    # populate webpage with queried entries
    return render_template('order.html', order=order, order_line=order_line, product=product)

@app.route('/add_order_line', methods=['POST', 'GET'])
def addOrderLine():
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM orders")
    order = cursor.fetchall()
    cursor.execute("SELECT * FROM order_lines")
    order_line = cursor.fetchall()
    cursor.execute("SELECT * FROM products")
    product = cursor.fetchall()
    if request.method == "POST":
        # fetch data from form inputs
        orderid = request.form['orderid']
        barcode = request.form['barcode']
        price = request.form['price']
        quantity = request.form['quantity']
        try:
            # call mysql stored procedure and commit changes
            cursor.callproc('add_order_line', (orderid, barcode, price, quantity))
            connection.commit()
            cursor.close()
            return redirect('/order')
        except Exception as e:
            flash(f'Cannot add order line: {e}')
    cursor.close()
    # populate webpage with queried entries
    return render_template('order.html', order=order, order_line=order_line, product=product)

@app.route('/deliver_order', methods=['POST', 'GET'])
def deliverOrder():
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM order_lines")
    order_line = cursor.fetchall()
    cursor.execute("SELECT * FROM orders")
    order = cursor.fetchall()
    cursor.execute("SELECT * FROM products")
    product = cursor.fetchall()
    if request.method == "POST":
        # fetch data from form inputs
        orderid = request.form['orderid']
        try:
            # call mysql stored procedure and commit changes
            cursor.callproc('deliver_order', (orderid,))
            connection.commit()
            cursor.close()
            return redirect('/order')
        except Exception as e:
            flash(f'Cannot deliver order: {e}')
    cursor.close()
    # populate webpage with queried entries
    return render_template('order.html', order=order, order_line=order_line, product=product)

@app.route('/cancel_order', methods=['POST', 'GET'])
def cancelOrder():
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM order_lines")
    order_line = cursor.fetchall()
    cursor.execute("SELECT * FROM orders")
    order = cursor.fetchall()
    cursor.execute("SELECT * FROM products")
    product = cursor.fetchall()
    if request.method == "POST":
        # fetch data from form inputs
        orderid = request.form['orderid']
        try:
            # call mysql stored procedure and commit changes
            cursor.callproc('cancel_order', (orderid,))
            connection.commit()
            cursor.close()
            return redirect('/order')
        except Exception as e:
            flash(f'Cannot cancel order: {e}')
    cursor.close()
    # populate webpage with queried entries
    return render_template('order.html', order=order, order_line=order_line, product=product)

@app.route('/view')
def view():
    return render_template("views.html")

@app.route("/customer_credit_check")
def customer_credit_check():
    cursor = connection.cursor()
    try:
        query = """
            SELECT uname AS Customer_Name, rating, credit,
            IFNULL((SELECT SUM(price * quantity) FROM orders JOIN order_lines ON orders.orderID = order_lines.orderID WHERE purchased_by = customers.uname), 0) AS credit_already_allocated
            FROM customers
            GROUP BY uname;
        """
        cursor.execute(query)
        value = cursor.fetchall()
    finally:
        cursor.close()
    return render_template("customer_credit_check.html", data=value, name='Customer Credit Check')

@app.route("/role_distribution")
def role_distribution():
    cursor = connection.cursor()
    try:
        query = """
            SELECT 'Users' AS Category, COUNT(*) AS Total FROM users
            UNION ALL
            SELECT 'Customers', COUNT(*) FROM customers
            UNION ALL
            SELECT 'Employees', COUNT(*) FROM employees
            UNION ALL
            SELECT 'Customer-Employer Overlap', COUNT(*) FROM customers NATURAL JOIN employees
            UNION ALL
            SELECT 'Drone Pilots', COUNT(*) FROM drone_pilots
            UNION ALL
            SELECT 'Store Workers', COUNT(*) FROM store_workers
            UNION ALL
            SELECT 'Other Employee Roles', COUNT(*) FROM employees WHERE uname NOT IN (SELECT uname FROM drone_pilots) AND uname NOT IN (SELECT uname FROM store_workers)
        """
        cursor.execute(query)
        value = cursor.fetchall()
    finally:
        cursor.close()
    return render_template("role_distribution.html", data=value, name='Role Distribution')

@app.route("/drone_traffic_control")
def drone_traffic_control():
    cursor = connection.cursor()
    query = "SELECT drone_serves_store, drone_tag, pilot, total_weight_allowed, current_weight, deliveries_allowed, deliveries_in_progress FROM drone_traffic_control;"
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    return render_template("drone_traffic_control.html", data=data, name='Drone Traffic Control')

@app.route("/most_popular_products")
def most_popular_products():
    cursor = connection.cursor()
    cursor.execute("select products.barcode, pname, weight, min(price), max(price), ifnull(min(quantity),0), ifnull(max(quantity),0), ifnull(sum(quantity),0) from products left join order_lines on products.barcode=order_lines.barcode group by products.barcode;")
    value = cursor.fetchall()
    cursor.close()
    return render_template("most_popular_products.html", data = value, name = 'most_popular_products')

@app.route("/drone_pilot_roster")
def drone_pilot_roster():
    cursor = connection.cursor()
    cursor.execute("select uname, licenseID, storeID, droneTag, experience, count(orderID) from drone_pilots left join drones on uname=pilot left join orders on droneTag=carrier_tag and storeID=carrier_store group by uname,storeID,droneTag;")
    value = cursor.fetchall()
    cursor.close()
    return render_template("drone_pilot_roster.html", data = value, name = 'drone_pilot_roster')

@app.route("/store_sales_overview")
def store_sales_overview():
    cursor = connection.cursor()
    cursor.execute("select storeID, sname, manager, revenue, ifnull(sum(price * quantity),0), ifnull(count(distinct orders.orderID), 0) from stores left join orders on storeID=carrier_store left join order_lines on orders.orderID=order_lines.orderID group by storeID;")
    value = cursor.fetchall()
    cursor.close()
    return render_template("store_sales_overview.html", data = value, name = 'store_sales_overview')


@app.route("/orders_in_progress")
def orders_in_progress():
    cursor = connection.cursor()
    cursor.execute("""
        SELECT orders.orderID, IFNULL(SUM(price * quantity), 0) AS cost, 
        IFNULL(COUNT(barcode), 0) AS num_products, 
        IFNULL(SUM(weight * quantity), 0) AS payload, GROUP_CONCAT(pname) AS contents
        FROM orders 
        LEFT JOIN order_lines ON orders.orderID = order_lines.orderID 
        NATURAL JOIN products 
        GROUP BY order_lines.orderID;
    """)
    value = cursor.fetchall()
    cursor.close()
    return render_template("orders_in_progress.html", data=value, name='Orders in Progress')

@app.route('/')
def main():
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)
    