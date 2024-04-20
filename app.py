from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from cryptography.fernet import Fernet
from decimal import Decimal

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '6502'
app.config['MYSQL_DB'] = 'hotwax'
mysql = MySQL(app)

# Encryption/Decryption key
key = b'VGvSzmbWrSh9ws4ATbU4CKqtu58VT3swoXn07__pu1E='
cipher_suite = Fernet(key)

# Encryption function
def encrypt_data(data):
    return cipher_suite.encrypt(data.encode())

# Decryption function
def decrypt_data(data):
    return cipher_suite.decrypt(data).decode()

# Common function to execute MySQL queries
def execute_query(query, data=None):
    try:
        cur = mysql.connection.cursor()
        if data:
            cur.execute(query, data)
        else:
            cur.execute(query)
        mysql.connection.commit()
        result = cur.fetchall()
        cur.close()
        return result
    except Exception as e:
        raise e
    

@app.route('/')
def hello_world():
    return 'Hello, World!'


# Route for creating a new person
@app.route('/create_person', methods=['POST'])
def create_person():
    try:
        person_data = request.json
        
        # Validate person data
        required_fields = ['party_id', 'first_name', 'last_name', 'gender', 'birth_date']
        for field in required_fields:
            if field not in person_data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        query = "INSERT INTO person (party_id, first_name, middle_name, last_name, gender, birth_date, marital_status_enum_id, employment_status_enum_id, occupation) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        data = (person_data['party_id'], person_data['first_name'], person_data.get('middle_name'), person_data['last_name'], person_data['gender'], person_data['birth_date'], person_data.get('marital_status_enum_id'), person_data.get('employment_status_enum_id'), person_data.get('occupation'))
        
        execute_query(query, data)

        return jsonify({'message': 'Person created successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

# Route for creating a new order
@app.route('/order/create_order', methods=['POST'])
def create_order():
    try:
        order_data = request.json

        # Encrypt credit card data before insertion
        encrypted_credit_card = encrypt_data(order_data.get('credit_card', ''))
        
        # Validate required fields
        required_fields = ['order_id', 'order_name', 'placed_date', 'party_id']
        for field in required_fields:
            if field not in order_data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Set default values for optional fields
        order_data.setdefault('currency_uom_id', 'USD')
        order_data.setdefault('status_id', 'OrderPlaced')
        
        query = "INSERT INTO order_header (order_id, order_name, placed_date, approved_date, status_id, party_id, currency_uom_id, product_store_id, sales_channel_enum_id, grand_total, completed_date, credit_card) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        data = (order_data['order_id'], order_data['order_name'], order_data['placed_date'], order_data.get('approved_date'), order_data['status_id'], order_data['party_id'], order_data['currency_uom_id'], order_data.get('product_store_id'), order_data.get('sales_channel_enum_id'), order_data.get('grand_total'), order_data.get('completed_date'), encrypted_credit_card)
        
        execute_query(query, data)

        order_id = execute_query("SELECT LAST_INSERT_ID()")[0][0]
        
        return jsonify({'orderId': order_id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

# Route for adding order items
@app.route('/order/add_items', methods=['POST'])
def add_order_items():
    try:
        data = request.json
        
        # Validate required fields
        required_fields = ['order_id', 'order_items']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        order_items = data['order_items']
        if not order_items:
            return jsonify({'error': 'No order items provided'}), 400
        
        for item in order_items:
            required_item_fields = ['product_id', 'quantity', 'unit_amount']
            for field in required_item_fields:
                if field not in item:
                    return jsonify({'error': f'Missing required field in order item: {field}'}), 400
        
        query = "INSERT INTO order_item (order_id, order_item_seq_id, product_id, item_description, quantity, unit_amount, item_type_enum_id) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        
        for item in order_items:
            item_data = (data['order_id'], item['order_item_seq_id'], item['product_id'], item.get('item_description', ''), item['quantity'], item['unit_amount'], item.get('item_type_enum_id', ''))
            execute_query(query, item_data)

        order_id = data['order_id']
        order_item_seq_ids = [item['order_item_seq_id'] for item in order_items]
        
        return jsonify({'orderId': order_id, 'orderItemSeqIds': order_item_seq_ids}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Route for getting all orders
@app.route('/orders', methods=['GET'])
def get_orders():
    try:
        query = "SELECT * FROM order_header"
        rows = execute_query(query)

        # Format orders data
        # Format orders data
        formatted_orders = []
        for row in rows:
            order_data = {
                'order_id': row[0],
                'order_name': row[1],
                'placed_date': row[2].isoformat(),
                'approved_date': row[3].isoformat() if row[3] else None,
                'status_id': row[4],
                'party_id': row[5],
                'currency_uom_id': row[6],
                'product_store_id': row[7],
                'sales_channel_enum_id': row[8],
                'grand_total': float(row[9]),
                'completed_date': row[10].isoformat() if row[10] else None,
                'credit_card': decrypt_data(row[11]),  # Decrypt credit card data
                'order_items': []  # You need to fetch and format order items as well
            }

            # Fetch order items for the current order
            query = "SELECT * FROM order_item WHERE order_id = %s"
            order_items = execute_query(query, (row[0],))
            
            # Format and append order items to the order data
            formatted_order_items = []
            for item in order_items:
                item_data = {
                    'order_item_seq_id': item[1],
                    'product_id': item[2],
                    'item_description': item[3],
                    'quantity': float(item[4]),
                    'unit_amount': float(item[5]),
                    'item_type_enum_id': item[6]
                }
                formatted_order_items.append(item_data)
            
            order_data['order_items'] = formatted_order_items

            formatted_orders.append(order_data)

        return jsonify({'orders': formatted_orders}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Route for getting an order by orderId
@app.route('/order/<string:order_id>', methods=['GET'])
def get_order(order_id):
    try:
        cur = mysql.connection.cursor()
        query = "SELECT * FROM order_header WHERE order_id = %s"
        cur.execute(query, (order_id,))
        order = cur.fetchone()
        cur.close()

        if not order:
            return jsonify({'error': f'Order with ID {order_id} not found'}), 404

        order_data = {
            'order_id': order[0],
            'order_name': order[1],
            'placed_date': order[2].isoformat(),
            'approved_date': order[3].isoformat() if order[3] else None,
            'status_id': order[4],
            'party_id': order[5],
            'currency_uom_id': order[6],
            'product_store_id': order[7],
            'sales_channel_enum_id': order[8],
            'grand_total': float(order[9]),
            'completed_date': order[10].isoformat() if order[10] else None,
            'credit_card': decrypt_data(order[11]),  # Decrypt credit card data
            'order_items': [] 
        }
        
        query = "SELECT * FROM order_item WHERE order_id = %s"
        order_items = execute_query(query, (order[0],))
        
        formatted_order_items = []
        for item in order_items:

            # Convert quantity to float if it's numeric
            quantity = float(item[3]) if isinstance(item[3], Decimal) else None

            # Convert unit_amount to float if it's numeric
            unit_amount = float(item[4]) if isinstance(item[4], Decimal) else None

            # Then use quantity and unit_amount in your item_data dictionary
            item_data = {
                'order_item_seq_id': item[0],
                'product_id': item[1],
                'item_description': item[2],
                'quantity': quantity,
                'unit_amount': unit_amount,
                'item_type_enum_id': item[5]
            }
            formatted_order_items.append(item_data)
        
        order_data['order_items'] = formatted_order_items

        return jsonify(order_data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500




# Route for updating an order by orderId
@app.route('/order/update', methods=['PUT'])
def update_order():
    try:
        data = request.get_json()
        order_id = data.get('order_id')
        new_order_name = data.get('order_name')

        if not order_id:
            return jsonify({'error': 'Order ID is required'}), 400

        if not new_order_name:
            return jsonify({'error': 'New order name is required'}), 400

        query = "UPDATE order_header SET order_name = %s WHERE order_id = %s"
        data = (new_order_name, order_id)
        execute_query(query, data)

        query = "SELECT * FROM order_header WHERE order_id = %s"
        updated_order = execute_query(query, (order_id,))

        if not updated_order:
            return jsonify({'error': f'Order with ID {order_id} not found'}), 404

        updated_order_data = {
            'order_id': updated_order[0][0],
            'order_name': updated_order[0][1],
            'placed_date': updated_order[0][2].isoformat(),
            'approved_date': updated_order[0][3].isoformat() if updated_order[0][3] else None,
            'status_id': updated_order[0][4],
            'party_id': updated_order[0][5],
            'currency_uom_id': updated_order[0][6],
            'product_store_id': updated_order[0][7],
            'sales_channel_enum_id': updated_order[0][8],
            'grand_total': float(updated_order[0][9]),
            'completed_date': updated_order[0][10].isoformat() if updated_order[0][10] else None,
            'credit_card': decrypt_data(updated_order[0][11])
        }

        return jsonify(updated_order_data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500




if __name__ == '__main__':
    app.run(debug=True)
