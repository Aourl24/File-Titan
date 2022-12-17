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

c='Hello there'
print(c)