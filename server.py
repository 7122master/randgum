# encoding=utf-8
from flask import Flask, request

app = Flask(__name__, static_url_path='')

@app.route('/jielong')
def jielong():
    return { "param": request.args.get("name") }

@app.route('/zhuyun')
def zhuyin():
    return {}

# @app.route('/')
# def root():
#     return app.send_static_file('index.html')

if __name__ == "__main__":
    app.run()
