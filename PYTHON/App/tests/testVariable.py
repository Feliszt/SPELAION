import json

def populateList(fileName) :
    count = 0
    list = []
    with open(fileName, "r") as classesFile:
        while True:
            count += 1
            line = classesFile.readline()
            if not line:
                break
            line = line.strip()
            #print("{}: {}".format(count, line.strip()))
            name = line.split(',')[0]
            list.append(name)
    return list

# lists
listA = []
listB = []

listA = populateList("data/classesList.txt")
listB = populateList("D:/PERSO/_UTILS/cfg/imagenet.shortnames_1000.list")

c = 0
notFound = []
for el in listA:
    c += 1
    print("{} : {}".format(c, el))
    if any(el in s for num, s in enumerate(listB, start=1)):
        print()
    else :
        notFound.append(el)

print("Couldn't find :")
for el in notFound:
    print(el)
