import json

with open('db.json', 'r') as f:
    #c=f.read()
    c=json.load(f)
    print(c)

d=0
w=''
for i in c.split():
    w += i
    d+=1
    if i.endswith('}},'):
        w += '\n'
        d=0

with open('db.json', 'w')  as h:
    json.dump(w, h)
        
#print(w)
#print(help(str.split))
#print(d)