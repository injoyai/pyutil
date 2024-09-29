import g
import time


def _test_go():
    def _for():
        for x in range(1000):
            time.sleep(1)
            g.println(x)

    g.go(_for, args=())
    g.go(_for, args=())
    g.go(_for, args=())


_test_go()
