import os
import json

context_list=[]
resource_list=[]
with open("Resource.json", "r") as resoucefile:
    data = json.load(resoucefile)
with open("context.json", "r") as genfile:
    data1 = json.load(genfile)

for n in data["@graph"]:
    resource_list.append(n["@id"])
# print(resource_list)
for n in data1["@graph"]:
    context_list.append(n["@id"]) 
# print(context_list)
differce_list=list(set(resource_list)-set(context_list))
print(differce_list)