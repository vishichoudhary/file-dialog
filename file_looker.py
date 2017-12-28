import os, sys
path=os.getcwd()
li=os.listdir(path)
def filter(inp):
    files=[]
    dirts=[]
    for i in inp:
        temp=os.path.join(path,i)
        if os.path.isfile(temp):
            files.append(i)
        else:
            dirts.append(i)
    return files,dirts

files,dirts=filter(li)
print(files)
print(dirts)
