# encoding=utf-8
from flask import Flask, request
import jielong.jielong as jielong
import zhuyin.evaluate as zhuyin

app = Flask(__name__, static_folder='')

JL = jielong.Solver()
print('jielong build complete')
print('loading zhuyin...')
ZY = zhuyin.build()
print('zhuyin load complete')

@app.route('/')
def root():
    return app.send_static_file('index.html')

@app.route('/jielong')
def jielong():
    query = request.args.get('name')
    return { "result": JL.solve(query) }

@app.route('/zhuyin')
def zhuyin():
    query = request.args.get('name')
    return { "result": ZY.evaluate(query) }

if __name__ == "__main__":
    app.run()
