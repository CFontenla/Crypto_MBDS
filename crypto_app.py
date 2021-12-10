from flask import Flask

app = Flask(__name__)

@app.route('http://127.0.0.1:64710/')
@app.route('http://127.0.0.1:64713/')
@app.route('http://127.0.0.1:64716/')
def index():
    return "Hello World!"


if __name__ == "__main__":
    app.run()