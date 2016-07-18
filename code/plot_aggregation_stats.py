import csv

import numpy as np
import matplotlib.pyplot as plt

def main():

    file = "T1Does_the_source_centred_in_the_green_crosshairs_in_summary.csv"

    data = {"subject_id":[],"most_likely":[],"p(most_likely)":[],"shannon_entropy":[], \
            "mean_agreement":[],"median_agreement":[],"num_users":[]}

    with open(file,"rb") as csvFile:
        reader = csv.reader(csvFile)
        for line in reader:
            if "subject_id" in line:
                continue
            data["subject_id"].append(line[0])
            data["most_likely"].append(line[1])
            data["p(most_likely)"].append(float(line[2]))
            data["shannon_entropy"].append(float(line[3]))
            data["mean_agreement"].append(float(line[4]))
            data["median_agreement"].append(float(line[5]))
            data["num_users"].append(float(line[6]))

    bins = [x for x in np.arange(0,1.04,0.04)]



    print 

    plt.hist(np.array(data["p(most_likely)"])[np.where(np.array(data["most_likely"])=="Yes")], \
             bins=bins, label="Real", color="#FF0066", edgecolor="none")

    plt.hist(1-np.array(data["p(most_likely)"])[np.where(np.array(data["most_likely"])=="No")], \
             bins=bins, label="Bogus", color="#66FF33", edgecolor="none")

    plt.legend()

    plt.show()
    
    """
    plt.scatter(np.array(data["p(most_likely)"])[np.where(np.array(data["most_likely"])=="Yes")], \
                np.array(data["shannon_entropy"])[np.where(np.array(data["most_likely"])=="Yes")])

    plt.scatter(1-np.array(data["p(most_likely)"])[np.where(np.array(data["most_likely"])=="No")], \
                np.array(data["shannon_entropy"])[np.where(np.array(data["most_likely"])=="No")])

    plt.show()
    """

if __name__ == "__main__":
    main()
