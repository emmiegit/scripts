#!/usr/bin/env python2

def _n(x):
    if x == "": return 1
    if x == "-": return -1
    else: return int(x)

def polyparse(s, var='x', pwr='^'):
    if s == "": return {0: 0}
    r = {}
    s = s.replace(" ", "")
    s = s.replace("*", "")
    s = s.replace(pwr, "")
    if not s.startswith("-"):
        s = s.replace("-", "+-")
    for p in s.split("+"):
        if var not in p:
            if 0 in r.keys():
                r[0] += _n(p)
            else:
                r[0] = _n(p)
            continue
        cx = p.split(var)
        ex, co = _n(cx[1]), _n(cx[0])
        if ex in r.keys():
            r[ex] += co
        else:
            r[ex] = co
    return r

def shlist(r):
    x = r.keys()
    x.sort()
    l = []
    for i in xrange(r[0], r[-1]+1):
        try:
            l += [i, r[i]]
        except:
            l += [i, 0]
    return l

