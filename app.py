# this app is for testing health check app
# it will start a server on port 8000, provide 3 endpoints for testing purpose

from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/')
def index():
    return 'Welcome to the index page'


@app.route('/careers')
def careers():
    return 'Welcome to the careers page'


@app.route('/some/post/endpoint', methods=['POST'])
def post_endpoint():
    return jsonify(message='Success')


if __name__ == '__main__':
    app.run(port=8000)
