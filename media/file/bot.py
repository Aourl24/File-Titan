from ToyDatabase import OurlDB
from random import choice
import time

class Bot:

	def __init__(self,name):
		self.name=name
		self.brain={'Hi':'Hello,hw are you doing','am doing fine':'great to hear'}

	def train(self,b,c):
		self.brain[b]=c
		return f"Now I get it thanks"

	def request(self,word=None):
		if word:
			return self.response(b)
			
		else:
			b=input('')
			return self.response(b)

	def response(self,b):
		if b in self.brain.keys():
			j=self.brain[b]
			return j

		else:
			c=input("Sorry I don't understand what to say, but you can teach me what to say in case of next time")
			return self.train(b,c)

	def chat(self):
		return self.request()

	def automate(self):
		a=['Hi','am doing fine','thanks']
		for i in a:
			print(i)
			time.sleep(3)
			print(self.request(word=i))
			time.sleep(3)
		return 'Finished'

	def start(self):
		intro=f'Hi buddy, Hw may i help you by the way my name is {self.name}'
		print(intro)

		while True:
			print(self.chat())

		return 'Done'


a=Bot('Awwal')
a.start()