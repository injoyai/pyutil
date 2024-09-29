import g

c = g.Chan(1)


g.go_do_after(c.append, "ggg1", 1.1)

g.select(
    c, print,
    g.Chan(1), print,
    g.Chan(1), print,
    default=print,
)

g.go_do_after(c.append, "ggg2", 1.2)

g.select(
    c, print,
    g.Chan(1), print,
    g.Chan(1), print,
)

g.select(
    c, print,
    g.Chan(1), print,
    g.Chan(1), print,
)
