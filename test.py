import zhuyin.evaluate as zhuyin

ZY = zhuyin.build()
print('build OK')

while True:
    try:
        S = input()
        print(ZY.evaluate(S))
    except EOFError:
        break


