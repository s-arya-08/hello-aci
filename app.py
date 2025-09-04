from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello from Azure Container Instances via Jenkins Pipeline! Updated on 05 Septemeber 2025 - v2"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
