import re
import json

master=[]
with open("mohan.txt") as f:
    arr=f.read().split("\n")
    for items in arr:
        al=re.findall(r'[\-0\.-9]+\s*',items)
        if not len(al):
            break
        dicter={"lat":al[2],"long":al[3],"cellno":al[1]}
        master.append(dicter)
    fr=open("master.json","w")
    fr.write(json.dumps(master))
    fr.close()

