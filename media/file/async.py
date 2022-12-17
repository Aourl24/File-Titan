import asyncio

async def wait():
	x='20'
	return int(x)

async def pun():
	b=await wait()
	return b


#answer=input('Choose your anwer')
#b=input('Choose your Number')

async def checkA(x):
	if isinstance(x,int):
		print('passed')
		return 'passed'

async def check(x,b):
	if isinstance(x,str):
		await checkA(b)
	print('passed')
	return 'Passed'

asyncio.run(check('awwal',3))



