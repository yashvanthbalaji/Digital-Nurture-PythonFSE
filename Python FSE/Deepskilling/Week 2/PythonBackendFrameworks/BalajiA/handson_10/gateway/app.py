from flask import Flask, jsonify, request, Response
import requests as http_client

app = Flask(__name__)

# ── SERVICE REGISTRY 
# In production, this would be Consul, Kubernetes DNS, or Eureka.
# Here we hardcode the addresses for simplicity.
SERVICES = {
    'courses':  'http://127.0.0.1:5001',
    'students': 'http://127.0.0.1:5002'
}


def proxy_request(target_url):
    """Forward the current request to target_url and return the response."""
    try:
        response = http_client.request(
            method=request.method,
            url=target_url,
            # Forward all headers except Host
            headers={k: v for k, v in request.headers if k.lower() != 'host'},
            json=request.get_json(silent=True),
            params=request.args,
            timeout=10
        )
        return Response(
            response.content,
            status=response.status_code,
            content_type=response.headers.get('Content-Type', 'application/json')
        )
    except http_client.ConnectionError:
        return jsonify({'error': 'Downstream service unavailable', 'code': 'SERVICE_DOWN'}), 503
    except http_client.Timeout:
        return jsonify({'error': 'Downstream service timed out'}), 504


# ── GATEWAY ROUTES 
# /api/courses/* → Course Service (port 5001)
@app.route('/api/courses/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
@app.route('/api/courses/<path:path>', methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def course_gateway(path):
    if path:
        target = f"{SERVICES['courses']}/api/courses/{path}"
    else:
        target = f"{SERVICES['courses']}/api/courses/"
    return proxy_request(target)


# /api/students/* → Student Service (port 5002)
@app.route('/api/students/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
@app.route('/api/students/<path:path>', methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def student_gateway(path):
    if path:
        target = f"{SERVICES['students']}/api/students/{path}"
    else:
        target = f"{SERVICES['students']}/api/students/"
    return proxy_request(target)


@app.route('/')
def root():
    return jsonify({
        'message': 'API Gateway running',
        'routes': {
            '/api/courses/*': f"→ Course Service ({SERVICES['courses']})",
            '/api/students/*': f"→ Student Service ({SERVICES['students']})"
        }
    })


if __name__ == '__main__':
    app.run(port=5000, debug=True)