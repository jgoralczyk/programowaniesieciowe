b = 4
def f3(a):
    global b
    print(a)
    print(b)
    b += 7
    print(b)


f3(3)