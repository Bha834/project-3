from flask import Flask, jsonify, request
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

# Prometheus metrics
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP Requests', ['service','endpoint','method','http_status'])
REQUEST_LATENCY = Histogram('http_request_latency_seconds', 'Request latency seconds', ['service','endpoint'])

SERVICE_NAME = "order-service"

# Dummy orders
orders = [
    {"id": 1, "user_id": 1, "item": "Laptop", "price": 50000},
    {"id": 2, "user_id": 2, "item": "Mobile", "price": 15000}
]

@app.route('/health')
def health():
    return jsonify({"status": "ok", "service": SERVICE_NAME})

@app.route('/orders', methods=['GET'])
def get_orders():
    with REQUEST_LATENCY.labels(SERVICE_NAME, "/orders").time():
        REQUEST_COUNT.labels(SERVICE_NAME, "/orders", 'GET', '200').inc()
        return jsonify({"orders": orders})

@app.route('/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    with REQUEST_LATENCY.labels(SERVICE_NAME, "/orders/<id>").time():
        order = next((o for o in orders if o["id"] == order_id), None)
        if order:
            REQUEST_COUNT.labels(SERVICE_NAME, "/orders/<id>", 'GET', '200').inc()
            return jsonify(order)
        REQUEST_COUNT.labels(SERVICE_NAME, "/orders/<id>", 'GET', '404').inc()
        return jsonify({"error": "Order not found"}), 404

@app.route('/orders', methods=['POST'])
def create_order():
    with REQUEST_LATENCY.labels(SERVICE_NAME, "/orders").time():
        data = request.get_json()
        new_order = {
            "id": len(orders) + 1,
            "user_id": data["user_id"],
            "item": data["item"],
            "price": data["price"]
        }
        orders.append(new_order)
        REQUEST_COUNT.labels(SERVICE_NAME, "/orders", 'POST', '201').inc()
        return jsonify(new_order), 201

@app.route('/metrics')
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
