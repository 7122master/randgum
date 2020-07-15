# encoding=utf-8
from flask import Flask, request
import jielong.jielong as jielong
import zhuyin.evaluate as zhuyin

app = Flask(__name__)

JL = jielong.Solver()
print('jielong build complete')
print('loading zhuyin...')
ZY = zhuyin.build()
print('zhuyin load complete')
# ZY.evaluate(testing_word)

@app.route('/jielong')
def jielong():
    query = request.args.get('query')
    return { "result": JL.solve(query) }

@app.route('/zhuyin')
def zhuyin():
    query = request.args.get('query')
    return { "result": ZY.evaluate(query) }

# @app.route('/')
# def root():
#     return app.send_static_file('index.html')

if __name__ == "__main__":
    app.run()
