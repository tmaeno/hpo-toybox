import sys
import json

src = sys.argv[1]
dst = sys.argv[2]

with open(src) as f:
    pars = json.load(f)

for par in pars:
    pars[par] = int(pars[par])

with open(dst, 'w') as f:
    json.dump(pars, f)
