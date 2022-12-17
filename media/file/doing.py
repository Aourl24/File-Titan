import timeit

a=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]

def search(x,b):
	for i in x:
		if i == b:
			return i
	return None


def searchA(x,b):
	if  b in x:
		return b
	return None

def searchB(x,b):
	L=len(x)/2

	if b < L:
		for i in x[:int(L)]:
			if i == b:
				return i
	elif b > L:
		for i in x[int(L):]:
			if i == b:
				return i

def searchC(x,b):
	L=len(x)/2
	L=4
	if b < L:
		if b in x[:L]:
			return b
		
	elif b > L:
		if b in x[L:]:
			return b

j=timeit.timeit('search(a,20)','from doing import search,a',number=1)
p=timeit.timeit('searchA(a,20)','from doing import searchA,a',number=1)
v=timeit.timeit('searchB(a,20)','from doing import searchB,a',number=1)
k=timeit.timeit('searchC(a,20)','from doing import searchC,a',number=1)
print('search',j)
print('searchA',p)
#h=searchB(a,3)
print('searchB',v)
print('searchC',k)
