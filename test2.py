



myset = set([1,2,3])

mylist = [ set([4,5,6]),set([1,3,2])]


print("mylist is {}".format(mylist))


test = False

if myset in mylist:
    test = True
print("test is {}".format(test))