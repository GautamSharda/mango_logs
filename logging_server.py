from flask import Flask, request

app = Flask(__name__)

@app.route('/log', methods=['POST'])
def log():
    message = request.get_data(as_text=True)
    print({message.message})
    return "Log received", 200

@app.route('/test', methods=['GET'])
def test():
    return "Test successful", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

