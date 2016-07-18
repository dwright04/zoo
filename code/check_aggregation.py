import csv
import ujson
import numpy as np

from collections import Counter

def main():

    classFile = "../../supernova-hunters-classifications-3.csv"
    aggFile   = "T1Does_the_source_centred_in_the_green_crosshairs_in_summary.csv"
    #aggFile   = "T1Does_the_source_centred_in_the_green_crosshairs_in.csv"
    subjectToVotes = {}
    with open(classFile,"rb") as csvFile:
        reader = csv.reader(csvFile)
        for line in reader:
            if "classification_id" in line:
                continue
            subjectData = ujson.loads(line[-2])
            metaData = ujson.loads(line[-4])
            live = metaData["live_project"]
            subjectId = str(subjectData.keys()[-1]).strip()
            vote = ujson.loads(line[-3])[0]["value"]
            # deal with labels from workflow changes
            if vote not in ["Yes", "No"] or not live:
                continue
                #if vote == "Real":
                #    vote = "Yes"
                #elif vote == "Bogus":
                #    vote = "No"
            try:
                #if len(subjectToVotes[subjectId]["votes"]) == 10:
                #    continue
                subjectToVotes[subjectId]["votes"].append(vote)
            except KeyError:
                subjectToVotes[subjectId] = {"votes":[vote]}

    csvFile.close()
    tmp  = []
    tmp2 = []
    #output = open("my_aggregations.csv","w")
    with open(aggFile,"rb") as csvFile:
        reader = csv.reader(csvFile)
        for line in reader:
            if "subject_id" in line:
                continue
        
            subjectId = str(line[0])
            try:
                votes = subjectToVotes[subjectId]["votes"]
                #print votes
            except KeyError:
                continue

            count = Counter(votes)
            num_users = len(votes)
            most_likely = count.most_common()[0][0]
            p_most_likely = count.most_common()[0][1] / float(num_users)
            print line[0], float(line[2]), p_most_likely, line[-1], num_users, np.allclose(float(line[2]), p_most_likely), int(line[-1])==num_users
            #print float(line[-1]) > num_users
            tmp.append(int(line[-1]))
            tmp2.append(num_users)
    print np.max(tmp), np.max(tmp2)

if __name__ == "__main__":
    main()
