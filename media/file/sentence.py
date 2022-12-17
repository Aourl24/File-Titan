from PyDictionary import PyDictionary
import csv
import pickle
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
        dic=PyDictionary()
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
            
#print(deep('what is is'))
#with open('verb.csv','r') as file:
#    csvreader=csv.reader(file)
#    for row in csvreader:
#        print(row)

b=Token()

#while True:
#    c=input()
#    f=b.deep(c)
#    print(f)
#    if c == 'exit':
#        break

def load():
    with open('dataset/computers.yml', 'r') as j:
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

d=tob()
print(d)
#save(d,'bot_database', 'wb')
        