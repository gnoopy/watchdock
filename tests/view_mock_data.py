import shelve
import pickle
import cPickle
import pprint

a={}


f=open('tests/mockdata.pkl','rb')
a=cPickle.load(f)
print("a keys ====>",a.keys())
# pp = pprint.PrettyPrinter(indent=4)
# pp.pprint(a)

# d = shelve.open('tests/mockdata.json')
# f=open('tests/mockdata.pkl','wb')
# for k in d.keys():
#     v = d[k]
#     a[k]=v 
# pickle.dump(a,f)


# f.close()


# print("All data -------------------\n"+str(d))
# del d['a']
# del d['b']
# set values
# myData['a'] = 1
# myData['b'] = 3

# # check for values.
# for keyVar in myData:
#     print(keyVar)
# # save the data for future use.
# myData.close()
# d.close()