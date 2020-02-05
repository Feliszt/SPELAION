# get indexes
def getLabelsFromFile(_fileName) :
    list = []
    with open(_fileName, "r") as classesFile:
        while True:
            line = classesFile.readline()
            if not line:
                break
            line = line.strip()
            name = line.split(',')[0]
            name = name.replace(' ', '_')
            name = name.replace("'", "")
            name = name.lower()
            list.append(name)
    return list

# image net labels
imageNetLabels = getLabelsFromFile("D:/TOAST/SPELAION/PYTHON/App/data/classesList_Inceptionv3.txt")

# write file
with open("D:/TOAST/SPELAION/PYTHON/App/data/classesListFull.txt", 'w') as f:
    for item in imageNetLabels:
        f.write("%s\n" % item)
