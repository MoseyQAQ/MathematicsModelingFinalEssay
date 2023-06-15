import itertools
from sys import argv
from joblib import Parallel,delayed
import numpy as np #代码行数过多，完整代码请见：https://github.com
import datetime 
import random
def get_feedback(guess, answer):
    b=0
    a = sum(1 for i in range(4) if guess[i] == answer[i])
    for i in range(4):
        if (guess[i] in answer) and (guess[i]!=answer[i]):
            b+=1
    #b = len(set(guess) & set(answer)) - a
    return f'{a}A{b}B'
def init(method=None):
    ch = ["0","1","2","3","4","5","6","7","8","9"]
    if method==1:
        return ch[np.random.randint(0,10,1)[0]]*4
    elif method == 2 :
        a=ch[np.random.randint(0,10,1)[0]]
        b=ch[np.random.randint(0,10,1)[0]]
        while a==b: 
            b=ch[np.random.randint(0,10,1)[0]]
        loc = np.random.randint(0,4,1)[0]
        return a*loc+b+ a*(3-loc)
    elif method == 4:
        ran=random.sample(ch,4)
        return ran[0]+ran[1]+ran[2]+ran[3]
    elif method== 31:
        ran=random.sample(ch,3)
        a1=ran[0]
        a2=ran[0]
        b=ran[1]
        c=ran[2]
        loc=random.sample(range(0,4),4)
        an=[None,None,None,None]
        an[loc[0]]=a1 
        an[loc[1]]=a2 
        an[loc[2]]=b 
        an[loc[3]]=c 
        return "".join(an)
    elif method==32:
        ran=random.sample(ch,2)
        a=ran[0]
        b=ran[1]
        loc=random.sample(range(0,4),4)
        an=[None,None,None,None]
        an[loc[0]]=a
        an[loc[1]]=a 
        an[loc[2]]=b 
        an[loc[3]]=b 
        return "".join(an)
    ini = np.random.randint(0,10,4)
    ini = ch[ini[0]]+ch[ini[1]]+ch[ini[2]]+ch[ini[3]]
    return ini 

def efficientminimax(guess,feedback,all_possble):
    possible = set()
    id=[]
    c=[0,0,0,0,0]
    for num in all_possble:
        if get_feedback(guess,num) == feedback:
            possible.add(num)
            i = identify(num)
            if i==4:
                c[0]+=1
            elif i==31:
                c[1]+=1
            elif i==32:
                c[2]+=1
            elif i==2:
                c[3]+=1
            elif i==1:
                c[4]+=1
            else:
                print("error in minimax")
                exit(-1)
            id.append(i)
    return possible,id,c

def identify(st):
    di = {}
    for i in range(4):
        if st[i] in di:
            di[st[i]] += 1
        else:
            di[st[i]]=1
    v = di.values()
    if len(di)==1:
        return 1
    elif len(v)==2 and 3 in v and 1 in v:
        return 2
    elif len(v)==3 and 2 in v and 1 in v: 
        return 31 
    elif len(v)==4:
        return 4
    else:
        return 32

def efficientrun(x,me=4):
    print(x)
    guesses = []
    all_possible = set(map(''.join, itertools.product('0123456789', repeat=4)))
    possible = set()
    ans=init()
    feedbacks = []
    c=0
    while True:
        c+=1 
        if len(guesses)==0:
            guess=init(4)
        guesses.append(guess)
        feedback = get_feedback(guess=guess,answer=ans)
        if feedback[0] == '4':
            return c 
        feedbacks.append(feedback)
        possible,id,count=efficientminimax(guess, feedback,all_possible)
        all_possible = possible.copy()
        if count[0]!=0:
            guess = list(all_possible).pop(id.index(4))
        elif count[1]!=0:
            guess = list(all_possible).pop(id.index(31))
        elif count[2]!=0:
            guess = list(all_possible).pop(id.index(32))
        elif count[3]!=0:
            guess = list(all_possible).pop(id.index(2))
        elif count[4]!=0:
            guess = list(all_possible).pop(id.index(1))
        else:
            print("error in run")
            exit(-1)
        all_possible.remove(guess)

def dryrun(x,init=init):
    ans=init()
    guess=init()
    c=0
    print(x)
    while True:
        c+=1
        feedback=get_feedback(guess,ans)
        if feedback[0]=='4':
            return c 
        guess = init()


def bench():
    start = datetime.datetime.now()
    result=Parallel(n_jobs=10)(delayed(dryrun)(x)for x in range(10000))
    end=datetime.datetime.now()
    print(f"time:{(end-start).seconds},ave:{np.mean(result)},\nstd:{np.std(result)}")
    np.savetxt("4.4-dry.txt",result)
    return 0

bench()

import numpy as np 
import matplotlib.pyplot as plt 
import seaborn as sns 
a=np.loadtxt("4.2-st.txt")
b=np.loadtxt("4.4-dry.txt")
sns.kdeplot(a,fill=True,bw_method=1)
plt.xlabel('Number of Times',fontsize=13)
plt.ylabel("Density",fontsize=13)
plt.savefig("1.svg")