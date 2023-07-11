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
