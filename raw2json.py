import re
import json

def process(path):

    master={"children":[]}

    with open(path) as f:
        content=f.read()
        arr=content.split("[,2]\n")[1].split("\n")
        import pdb; pdb.set_trace()
        nrow,ncol=arr[len(arr)-1].split('"')[1].split(" ")
        master["nrow"]=nrow
        master["ncol"]=ncol
        arr.pop()
        for items in arr:
            al=re.findall(r'[\-0\.-9]+\s*',items)
            if not len(al):
                break
            dicter={"lat":al[2],"long":al[3],"cellno":al[1]}
            master["children"].append(dicter)
    
    return master


