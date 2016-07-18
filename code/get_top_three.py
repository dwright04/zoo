import ujson, csv
import numpy as np
from datetime import datetime

users = []
timestamps = []
labels = []
subjects = []
with open("1205028440040317000_classifications.txt","rb") as csvFile:
    reader = csv.reader(csvFile)
    for line in reader:
        subjects.append(line[-1])
        users.append(line[1])
        data = ujson.loads(line[10])
        print data["finished_at"].replace("T"," ").replace("Z","")
        timestamps.append(datetime.strptime(data["finished_at"].replace("T"," ").replace("Z",""), "%Y-%m-%d %H:%M:%S.%f"))
        data = ujson.loads(line[-3])
        #print data[0]["value"]
        labels.append(data[0]["value"])

print subjects
print len(subjects)
list1, list2, list3 = zip(*sorted(zip(timestamps, users, labels)))
print list2
list3 = [str(x) for x in list3[:]]
print list3
print len(list3)
print np.array(list3) == "Yes"
print np.array(list1)[np.array(list3)=="Yes"]
print np.array(list2)[np.array(list3)=="Yes"]
print np.array(list3)[np.array(list3)=="Yes"]
