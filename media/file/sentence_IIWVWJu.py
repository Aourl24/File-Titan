#from PyDictionary import PyDictionary
import csv
import pickle
from random import choice
#from mybot import save
#import yaml

class Token:

    def __init__(self):
        self.ability=[]
        self.about={'name':'adiva', 'age':'2022'}
        self.aux=['sing', 'dance', 'fly']
        self.person={'owner':'awwal'}
        self.place={'live':'Nigeri'}

    def _about(self, x):
        return f'my {x} is {self.about[x]}'
           
    def deep(self, x):
        aux_verb=['can', 'is', 'am', 'are', 'were', 'being', 'been','has', 'have', 'had','shall', 'will', 'should','may', 'might','must'
        'could', 'does', 'do', 'was', 'be', 'did', 'would']
        #dic=PyDictionary()
        dic=''
        ability=['']
        splitx=x.split()
        
        #if 'you' in splitx:
            
        if x.startswith('what is') or x.startswith('what are'):
            if x.startswith('what is your') or x.startswith('what are your'):
                if splitx[3] in self.about.keys():
                   return self._about(splitx[3])
            
            if x.startswith('what is the') or x.startswith('what is a'):
                meaning=dic.meaning(d[3])
                return meaning
        
        for word in aux_verb:
            if x.startswith(word):
                if splitx[2] in self.aux:
                    return f'yes , i {word} {splitx[2]}'
                else:
                    return f'no , i {word} not {splitx[2]}'
        return 'This word is not a question word'
            

    def phrase(self,x,g):
        x=x.split()
        lenx=len(x)
        likely_words=[]
        m=[]
        c=0
        l=[u.lower() for u in g]
        a=l[c]

        while a:
            for i in a.split():
                i=i.replace('?','')
                i=i.replace('.','')
                #print(i)
            
                if i in x :
                    m.append(i)

            if len(set(m)) >= 3:
                likely_words.append(a)
            
            if c == len(l):
                a=False
            else:
                c+=1
                a=l[c]
                m=[]
        
        print(likely_words)
        try:
            cho=choice(likely_words)
        except:
            cho='I had no Idea of this question'
        return cho

    def answer(self,x,l):
        b=self.deep(x.lower())

        if b == 'This word is not a question word':
            k=self.phrase(x.lower(),[j.lower() for j in l.keys()])
            if k != 'I had no Idea of this question':
                ans=l[('').join(list(filter(lambda x: x.lower() == k.lower(),l)))]
            else:
                ans=['I had no Idea of this question','I did not get your question',"I don't understand your question,try asking in another way"]    
            return choice(ans)
        elif b:
            return b
        else:
            return 'I have no idea about your question'






#b=Token()

#while True:
#    c=input()
#    f=b.deep(c)
#    print(f)
#    if c == 'exit':
#        break

def load():
    with open('dataset/emotion.yml', 'r') as j:
        c=j.read()
        
    return c

def tob():
    a=1
    with open('bot_database', 'rb') as m:
        store=pickle.load(m)
    print(store)       
    d=load()
    f=d.split('\n')
    try:
        for i in range(len(f)):
            if i%2 == 0:
                try:
                    store[f[i].strip('- -')].append(f[i+1].strip(' -'))
                except KeyError:
                    store[f[i].strip('- -')]=[]  
                    store[f[i].strip('- -')].append(f[i+1].strip(' -'))
    
    except IndexError:
        s=''
        for i in f:
            if i.startswith('- -'):
                 s=i.strip('- -')
                 store[i.strip('- -')]=[]
                 store[i.strip('- -')]=[]  
            else:
                store[s].append(i.strip(' -'))
            #store[f[i].strip('- -')].append(f[i+1].strip(' -'))
    
                 

        
       
    
    return store
    
def save(data, database, mode, ):
    with open(database,mode) as f:
        pickle.dump(data,f)
    print('done')
    return 'done'  

# d=tob()
# print(d)
# save(d,'bot_database', 'wb')
a='doing?'
a=a.replace('?','')
        