from random import*
a=randint(0,100)
N=1
while True:
    #try-except方法
    '''try:
        b=int(input('请猜一个数字：'))
    except:
        print('input error!')'''
    b=input('guess a number:')
    if not b.isdigit():
            print('input error!input again:')
            continue
    else:
        b=int(b)
    if b>a:
        print('too big,try again:')
        N+=1
        continue
    elif b<a:
        print('too small,try again:')
        N+=1
        continue
    else:
        print('bingo!')
        break
    
print('You have guessed {} times'.format(N))
    
