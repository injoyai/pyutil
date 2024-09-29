import time
import g


def _test_go():
    def _for():
        for x in range(1000):
            time.sleep(1)
            print(x)

    g.go(_for, args=())
    g.go(_for, args=())
    g.go(_for, args=())


def _test_chan():
    c = g.Chan()

    def add(n):
        c.append(n)

    g.go_interval(add)

    def get(n):
        g.println('get: ', c.get())

    g.go_interval(get, 0.1)

    g.println('start range')
    for x in c:
        g.println('range: ', x)
    g.println('end')


def _test_select():
    c1 = g.Chan()
    c2 = g.Chan()

    def add1(n):
        c1.append(f'c1: {n}')

    def add2(n):
        c2.append(f'c2: {n}')

    g.go_interval(add1)
    g.go_interval(add2, 5)

    # for x in g.for_select(g.after(1), c2):
    #     g.println(x)

    for i,x in g.range_select(c1, c2):
        g.println(i,x)

    pass


_test_select()
