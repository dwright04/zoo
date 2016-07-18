import csv, ujson

import numpy as np

from collections import Counter

def read_aggregation(file):

    data = {
            "subject_id":[], \

            }

    with open(file,"rb") as csvFile:
        reader = csv.reader(csvFile)
        for line in reader:
            if "subject_id" in line:
                continue
            """
            data[line[0]] = {
                                  "most_likely":[], \
                                  "p(most_likely)":[], \
                                  "shannon_entropy":[], \
                                  "mean_agreement":[], \
                                  "median_agreement":[], \
                                  "num_users":[]
                                  }
            """
            data[line[0]] = {}
            data[line[0]]["most_likely"] = line[1]
            data[line[0]]["p(most_likely)"] = float(line[2])
            data[line[0]]["shannon_entropy"] = float(line[3])
            data[line[0]]["mean_agreement"] = float(line[4])
            data[line[0]]["median_agreement"] = float(line[5])
            data[line[0]]["num_users"] = float(line[6])

    return data

def read_subject_sets(file):
    ps1IdToSubject = {}
    with open(file,"rb") as csvfile:
        reader = csv.reader(csvfile)
        for line in reader:
            if "subject_id" in line:
                continue
            jsonData = ujson.loads(line[4])
            #print jsonData
            try:
                refFile = jsonData["target"]
            except KeyError:
                continue
            objectId = refFile.split("_")[0]
            mjd = float(refFile.split("_")[1])
            if mjd < 57561:
                continue
            try:
                ps1IdToSubject[objectId].append(line[0])
            except KeyError:
                ps1IdToSubject[objectId] = []
                ps1IdToSubject[objectId].append(line[0])

    return ps1IdToSubject

def main():

    aggregationFile = "/Users/darrylwright/dev/zooniverse/data/classifications/2455/1737_Real_or_Bogus/T1Does_the_source_centred_in_the_green_crosshairs_in_summary.csv"

    subjectFile = "/Users/darrylwright/dev/zooniverse/data/subject_sets/supernova-hunters-subjects-5.csv"
    
    agreggationResults = read_aggregation(aggregationFile)
    #exit()
    ps1IdsToSubjects = read_subject_sets(subjectFile)

    objectClassifications = {}

    notRetiredCounter = 0
    #notRetired = []
    for id in ps1IdsToSubjects:
        #if id in set(notRetired):
        #    continue
        for subject in ps1IdsToSubjects[id]:
            try:
                agreggationResults[subject]
            except KeyError:
                print "[-] Subject %s not retired for %s" % (subject, id)
                try:
                    del objectClassifications[id]
                    #notRetired.append(id)
                except KeyError:
                    pass
                notRetiredCounter += 1
                break
            try:
                print "[+] Subject %s retired for %s" % (subject, id)
                objectClassifications[id]["most_likely"].append(agreggationResults[subject]["most_likely"])
                if agreggationResults[subject]["most_likely"] == "Yes":
                    objectClassifications[id]["P(real)"].append(agreggationResults[subject]["p(most_likely)"])
                elif agreggationResults[subject]["most_likely"] == "No":
                    objectClassifications[id]["P(real)"].append(1-agreggationResults[subject]["p(most_likely)"])
            except KeyError:
                #print "[+] Subject %s retired for %s" % (subject, id)
                print "[+] Adding key for %s" % (id)
                objectClassifications[id] = {"P(real)":[], "most_likely":[]}
                objectClassifications[id]["most_likely"].append(agreggationResults[subject]["most_likely"])
                if agreggationResults[subject]["most_likely"] == "Yes":
                    objectClassifications[id]["P(real)"].append(agreggationResults[subject]["p(most_likely)"])
                elif agreggationResults[subject]["most_likely"] == "No":
                    objectClassifications[id]["P(real)"].append(1-agreggationResults[subject]["p(most_likely)"])

    output = open("classifications_by_object_20160711_sinceJun22.csv","w")
    
    for id in objectClassifications:
        count = Counter(objectClassifications[id]["most_likely"])
        #if count.most_common()[0][1] == count.most_common()[1][1]:
        #    print "%s,%.3f" % (id, np.median(np.array(objectClassifications[id]["P(real)"])))
        #    output.write("%s,%.3f\n" % (id, np.median(np.array(objectClassifications[id]["P(real)"]))))
        #else:
        most_likely = count.most_common()[0][0]
        #print np.array(objectClassifications[id]["P(real)"])[np.where(np.array(objectClassifications[id]["most_likely"])==most_likely)]
        print "%s,%.3f" % (id, np.median(np.array(objectClassifications[id]["P(real)"])[np.where(np.array(objectClassifications[id]["most_likely"])==most_likely)]))
        #print "%s,%.3f,%.3f" % (id, np.median(np.array(objectClassifications[id]["P(real)"])), np.std(np.array(objectClassifications[id]["P(real)"])))
        #output.write("%s,%.3f\n" % (id, np.median(np.array(objectClassifications[id]["P(real)"]))))
        output.write("%s,%.3f\n" % (id, np.mean(np.array(objectClassifications[id]["P(real)"])[np.where(np.array(objectClassifications[id]["most_likely"])==most_likely)])))
    output.close()

    print "Not retired count: %d" % notRetiredCounter

if __name__ == "__main__":
    main()
