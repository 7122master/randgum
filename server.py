# encoding=utf-8
from flask import Flask, request
from jielong import Solver
import zhuyin

app = Flask(__name__, static_url_path='')

JL = Solver()

@app.route('/jielong')
def jielong():
    query = request.args.get("query")
    return { "result": JL.solve(query) }

@app.route('/zhuyin')
def zhuyin():
    return {}

# @app.route('/')
# def root():
#     return app.send_static_file('index.html')

if __name__ == "__main__":
    app.run()
