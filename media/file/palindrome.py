from timeit import default_timer as timer

f = ['palindrome', 'madamimadam', 'wow', 'foo', 'eyes']  
k = ['house','deed','paper','peep']
k =  ['house','deed','paper','peep']
f = [
'kayak',
'deified',
'rotator.',
'repaper',
'deed',
'peep',
'wow',
'noon'
]

def checkPali(x):
    check  = [True if ('').join(reversed(i)) == i else False for i in x]
    return check


start = timer()
print(checkPali(f))
end = timer()

print(end-start)

start_2 = timer()

total = []
for i in f:
    #d=reversed(i)
    #print(('').join(d))
    #e=('').join(list(d))
    e = ('').join(reversed(i))
    if e == i:
        total.append(True)
    else:
        total.append(False)
        
print(total)
start_3=timer()
print(start_3-start_2)

x = f

start_3= timer()
check  = [True if ('').join(reversed(i)) == i else False for i in x]

string = ['palindrome', 'madamimadam', 'wow', 'foo', 'eyes'] 
palindrome = [True if i[::-1] == i else False for i in string]
print(palindrome)
start_4 = timer()

print(start_4-start_3)