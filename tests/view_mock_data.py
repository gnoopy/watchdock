import shelve
d = shelve.open('./mockdata.json')


print("keys------------------------\n"+str(d.keys()))

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
d.close()