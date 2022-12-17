#from ToyDatabase import OurlDB
from random import choice
import time
import pickle
#import numpy as np
from datetime import datetime
from sentence import Token

class Bot(Token):

	def __init__(self,name):
		self.name , self.control = name, True,
		with open('bot_database','rb') as f:
		    self.brain=pickle.load(f)
		

	def _train(self,b,c):
		self.brain[b.lower().strip()] = []
		self.brain[b.lower().strip()].append(c.lower().strip())

		with open('bot_database','wb') as f:
			pickle.dump(self.brain, f)

		pass 

	def _acessMemory(self):
	    return self.brain
	    
	def trainTutorial(self):
		word_key = input('Key: ')
		if word_key == 'exit':
		    self.control = False
		    return self.train()
		    
		word_value = input('Value: ')
		return self._train(word_key,word_value)

	def train(self):
		while self.control:
			self.trainTutorial()
		return 'End of training Session'
		
	def calculate(self, val):
	    d=eval(val)
	    return d
	    
	def request(self,word=None):
		if word:
			return self.response(b)
			
		else:
			b=input('')
			return self.response(b)

	def _change(self, key):
		try:
			print('Old Key Values are',key,self.brain[key])
			g=input('Enter New Value ')
			self.brain.pop(key)
			self._train(key,g)
			print('New Value',key,self.brain[key])
			return  'Changed Succesfully'

		except KeyError:
			print(key,'does not Exist in database')
			
	def _del(self, key):
		try:
		    print('Old Key Values are',key,self.brain[key])
		    self.brain.pop(key)
		    with open('bot_database','wb') as f:
			    pickle.dump(self.brain, f)
			    
		except KeyError:
			print(key,'does not Exist in database')
		return 'Word is deleted Succeffully'
					
	def response(self,req):
		question=['is', 'a', 'an', 'to', 'did','the','of','are','what', 'where', 'how', 'who', 'what', 'when']
		common=['is', 'a', 'an', 'to', 'did','the','of']
		personal={'what is your name':f'My name is {self.name} ','what is the time':f'the time is {datetime.now().time()}','what is today':f'today is {datetime.now().date()}'}
		
		if req == 'quit':
			self.control = False
			return 'Bye'

		if req == '_change':
			changeVal=input('Key you want to change ')
			return self._change(changeVal)
			
		if req == '_train':
		    return self.train()
		    
		if req == '_del':
			delKey =input('Key you want to delete ') 
			return self._del(delKey)		

		if req == '_mem':
		    print(self._acessMemory())
		    
		if req in personal.keys():
			return personal[req]

		critical_word=''
		split_req= req.split()
		brain_keys= self.brain.keys()
		
		critical_value=''
		brain_values=self.brain.values()
		
		occur_dict={}


		for word in brain_keys:
			number_of_occur=contain(split_req,word,exp=question)
			occur_dict[number_of_occur] = word


			if len(split_req) == 1:
				if number_of_occur >= 1:
					critical_word=word
					break
					
		max_key = max(occur_dict.keys())
		if  'you' in split_req and len(split_req) >= 4 :
		    #critical_word=occur_dict[max_key]
		    if max_key >= 3:
		        critical_word=occur_dict[max_key]

		else:
		    #critical_word=occur_dict[max_key]
		    if max_key >= 2:
		        critical_word=occur_dict[max_key]
#			else:			
#				if number_of_occur >= 2:
#					critical_word=word
#					break
		
		
		#print('values',brain_values)
		#print('keys',brain_keys)
		for val in brain_values:
			for v in val:
				number_of_val_occur=contain(split_req, v,exp=common)

				if number_of_val_occur >= 3:
					critical_value=val
					break

		#print('value',critical_value)
		if req.lower() in (k.lower() for k in self.brain.keys()):
			replies=self.brain[('').join(list(filter(lambda x: x.lower() == req.lower(),self.brain)))]

			reply=choice(replies)
			return reply 
		
		elif critical_word:
			replies=self.brain[critical_word]
			reply=choice(replies)
			#self._train(req,reply)
			return reply

		else:
			
			c="Sorry I don't have any idea for that exact question,Do you have any Idea about it, Tell me"
			wrong=['no',"i don't have any idea",'no idea',"don't",'do not','no idea']
			if c.lower() in wrong:
				return "No Problem, You can ask another Question"
			
			#self._train(req,c)
			return c

	def chat(self):
		return self.request()

	def compare(self):
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

		while self.control:
			print(self.chat())

		return 'Done'


def contain(x,w,exp=None):
	count=0
	for i in x:
		if exp:
			if i in exp:
				pass
			else:
				if i in w:
					count +=1
		else:
			if i in w:
				count+=1

	return count


#a=Bot('Adiva')
#a.start()
#a.train()

def che():
    dic={}
    
    with open('train.txt', 'r') as j:
        answer=[]
        for i in j.readlines():
            d=i.split('\t')
            k=d[0]
            m=d[1]
            
            if k in dic.keys():
                dic[k].append(m)
                
            else:  
                
                dic[k]=[]
                dic[k].append(m)
            
        
    with open('bot_database','wb') as f:
        pickle.dump(dic, f)
    print('done')
    return 'done'
                

     