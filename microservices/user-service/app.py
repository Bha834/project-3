from flask import Flask, jsonify, request
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP Requests', ['service','endpoint','method','http_status'])
REQUEST_LATENCY = Histogram('http_request_latency_seconds', 'Request latency seconds', ['service','endpoint'])

SERVICE_NAME = "user-service"

@app.route('/health')
def health():
    return jsonify({"status":"ok","service":SERVICE_NAME})

@app.route('/user/<int:user_id>')
def get_user(user_id):
    with REQUEST_LATENCY.labels(SERVICE_NAME, "/user/<id>").time():
        # simulate logic
        REQUEST_COUNT.labels(SERVICE_NAME, "/user/<id>", 'GET', '200').inc()
        return jsonify({"id": user_id, "name": "User "+str(user_id)})

@app.route('/metrics')
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
