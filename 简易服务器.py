from flask import Flask,send_file

app = Flask(__name__)

@app.route('/')
def index():
    return send_file('index.html')

@app.route('/<path:filename>')
def filename(filename):
    return send_file(filename)


if __name__ == "__main__":
    app.run(debug=True)
