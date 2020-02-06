
# set variables
logFile = "D:/TOAST/SPELAION/PYTHON/App/data/logLabels.txt"
hist = {}

# compute hist
with open(logFile, 'r') as f:
    for line in f:
        if line.strip() not in hist:
            hist[line.strip()] = 1
        else :
            hist[line.strip()] = hist[line.strip()] + 1

# show hist
hist = {k: v for k, v in sorted(hist.items(), key=lambda item: item[1])}
for el in hist :
    print("{} => {}".format(el, hist[el]))
