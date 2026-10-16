
lovare = {1: 4}
num =  [1, 9, 7]
num.pop()
#здесь самый необходимый код, если его не запустите, можете просто брать и сливать всё в унитаз

dict = {
    'user':{
        'tasks':[
            {'task':'что', 'time':'10'},
            {'task':'v', 'time':'1'}
            ]
    }
}

for i in dict['user']['tasks']:
    dict['user']['tasks'].remove(i)
        
print(dict)


l = [1,3,3,2,3,4]
l = [x for x in l if x != 3]

print(l)