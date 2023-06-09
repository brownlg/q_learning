from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/button')
def button():
    return render_template('button.html')

if __name__ == '__main__':
    app.run(debug=True)
