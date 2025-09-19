from flask import Flask, jsonify, request

app = Flask(__name__)

# Dummy orders
orders = [
    {"id": 1, "user_id": 1, "item": "Laptop", "price": 50000},
    {"id": 2, "user_id": 2, "item": "Mobile", "price": 15000}
]

@app.route('/orders', methods=['GET'])
def get_orders():
    return jsonify({"orders": orders})

@app.route('/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    order = next((o for o in orders if o["id"] == order_id), None)
    if order:
        return jsonify(order)
    return jsonify({"error": "Order not found"}), 404

@app.route('/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    new_order = {
        "id": len(orders) + 1,
        "user_id": data["user_id"],
        "item": data["item"],
        "price": data["price"]
    }
    orders.append(new_order)
    return jsonify(new_order), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
