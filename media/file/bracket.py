a='(((())))(()())'
b='(())(()()()(()'
c='()()'
j='((()'
def Bracket(x):
	a=sorted(x)
	L=int(len(a)/2)
	originalFirst=a[:L]
	originalLast=a[L:]
	#print(originalFirst)
	for i in originalFirst:
		if i == ')':
			return False

	for i in originalLast:
		if i == '(':
			return False
	return True

k=Bracket(c)
v=Bracket(j)
d=Bracket(a)
e=Bracket(b)
print(d)
print(e)
print(k,v)