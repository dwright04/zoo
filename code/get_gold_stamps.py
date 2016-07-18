import scipy.io as sio
import numpy as np

from shutil import copy2

def main():

    filename = "/Users/dew/development/PS1-Real-Bogus/data/3pi_20x20_skew2_signPreserveNorm.mat"
    data = sio.loadmat(filename)

    print data.keys()

    mjds            = []
    files           = []
    labels          = []
    image_group_ids = []

    y = np.squeeze(data["y"])

    for i,file in enumerate(data["train_files"]):
        files.append(str(file).strip())
        mjds.append(str(file).strip().split("_")[1][:-4])
        image_group_ids.append(str(file).strip().split("_")[2])
        labels.append(y[i])

    y = np.squeeze(data["testy"])

    for i,file in enumerate(data["test_files"]):
        files.append(str(file).strip())
        mjds.append(str(file).strip().split("_")[1][:-4])
        image_group_ids.append(str(file).strip().split("_")[2])
        labels.append(y[i])

    print files[:10], mjds[:10], image_group_ids[:10], y[:10]

    

if __name__ == "__main__":
    main()
