import re
import json

def process(path):

    master={"nrow": 20 ,"ncol": 23 ,"children":[]}

    with open(path) as f:
        content=f.read()
        arr=content.split("[,2]\n")[1].split("\n")
        for items in arr:
            al=re.findall(r'[\-0\.-9]+\s*',items)
            if not len(al):
                break
            dicter={"lat":al[2],"long":al[3],"cellno":al[1]}
            master["children"].append(dicter)
    
    return master


process("output.txt")