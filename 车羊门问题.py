from random import *
seq=[0,0,1]
n1=n2=0
for i in range(10000):
    b=choice(seq)
    if b==1:
        n1+=1
        b=0
    else:
        b=1
    if b==1:
        n2+=1
print('原来的胜率：{:.2f}%，更改后：{:.2f}%'.format(n1/100,n2/100))
        
    
