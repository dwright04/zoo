import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

def main():

    ids = []
    humans = []
    machine = []
    for line in open("machine_classifications_by_object_20160711_sinceJun22.csv","r").readlines():
        if "#" in line:
            continue
        data = line.strip().split(",")
        ids.append(data[0])
        humans.append(float(data[1]))
        machine.append(float(data[2]))
        #if float(data[1]) > 0.9:
        #   print data[0], float(data[1])

    lists = {
             "confirmed" : [],
             "good"      : [],
             "possible"  : [],
             "attic"     : [],
             "zoo"       : [],
             "garbage"   : []
            }

    colourmap = {
                 "confirmed" : "#0014CE",
                 "possible"  : "#FCB606",
                 "good"      : "#F00200",
                 "attic"     : "#3D348B",
                 "zoo"       : "#011627",
                 "garbage"   : "#669D31"
                }

    for i,line in enumerate(open("web_info_classifications_by_object_20160711_sinceJun22.csv")):
        data  = line.split(",")
        lists[data[1]].append(i)

    real_machine = []
    real_human = []
    bogus_machine = []
    bogus_human = []
    fig = plt.figure()
    ax = fig.add_subplot(111)
    for key in ["garbage","attic","possible","zoo","good","confirmed"]:
        if lists[key] == []:
            continue
        ax.scatter([machine[x]*100 for x in lists[key]], [humans[x]*100 for x in lists[key]], color=colourmap[key], label=key)
        if key in ["good", "attic"]:
            for x in lists[key]:
                real_machine.append(machine[x])
                real_human.append(humans[x])
        elif key == "garbage":
            for x in lists[key]:
                bogus_machine.append(machine[x])
                bogus_human.append(humans[x])

    """
    plt.ylim(ymin=-0.01,ymax=1.01)
    plt.xlim(xmin=-0.01,xmax=1.01)
    plt.ylabel("human")
    plt.xlabel("machine")
    plt.legend(loc="upper left")
    plt.show()
    """
    nreal = len(real_machine)
    print nreal
    print len(humans)
    real_machine = np.array(real_machine)
    real_human = np.array(real_human)
    #print real_machine
    nbogus = len(bogus_machine)
    print nbogus
    bogus_machine = np.array(bogus_machine)
    bogus_human = np.array(bogus_human)

    im = np.zeros((1/.01 + 1, 1/.01 + 1))
    min = 2
    fpr_thresholds = None
    mdr_thresholds = None
    for i,machine_threshold in enumerate(np.arange(0,1.01, 0.01)):
        for j,human_threshold in enumerate(np.arange(0,1.01, 0.01)):
            mdr = len(np.unique(np.concatenate((np.where(real_machine<machine_threshold)[0], np.where(real_human<human_threshold)[0])))) / float(nreal)
            fpr = len(np.unique(np.concatenate((np.where(bogus_machine>=machine_threshold)[0], np.where(bogus_human>=human_threshold)[0])))) / float(nbogus)
            #print mdr, fpr
            """
            if mdr+fpr < min:
                min_thresholds = (machine_threshold, human_threshold)
                min_mdr = mdr
                min_fpr = fpr
                min = mdr+fpr
            """
            if fpr < 0.05 and fpr > 0.049 and fpr_thresholds is None:
                fpr_thresholds = (machine_threshold, human_threshold)
                print len(np.unique(np.concatenate((np.where(bogus_machine>=machine_threshold)[0], np.where(bogus_human>=human_threshold)[0]))))
            if mdr < 0.051 and mdr > 0.049 and mdr_thresholds is None:
                mdr_thresholds = (machine_threshold, human_threshold)
                print len(np.unique(np.concatenate((np.where(real_machine<machine_threshold)[0], np.where(real_human<human_threshold)[0]))))
            im[i,j] += mdr
    #print min_thresholds, min_mdr, min_fpr, min
    #plt.plot([min_thresholds[0]*100,min_thresholds[0]*100],[0*100,1*100],"r--")
    plt.plot([fpr_thresholds[0]*100,fpr_thresholds[0]*100],[0*100,1*100],"r--")
    plt.plot([mdr_thresholds[0]*100,mdr_thresholds[0]*100],[0*100,1*100],"b--")
    #plt.plot([0.436*100,0.436*100],[0*100,1*100],"r--")
    #plt.plot([0*100,1*100],[min_thresholds[1]*100,min_thresholds[1]*100],"r--")
    plt.plot([0*100,1*100],[fpr_thresholds[1]*100,fpr_thresholds[1]*100],"r--")
    plt.plot([0*100,1*100],[mdr_thresholds[1]*100,mdr_thresholds[1]*100],"b--")
    cax = ax.imshow(np.fliplr(np.rot90(im,3)),interpolation="nearest",cmap="gray",zorder=0)
    cbar = fig.colorbar(cax)
    plt.gca().invert_yaxis()
    ax.set_xticklabels([x for x in np.arange(-0.2,1.2,0.2)])
    ax.set_yticklabels([x for x in np.arange(-0.2,1.2,0.2)])
    plt.ylabel("human score")
    plt.xlabel("machine score")
    plt.legend(loc="upper left")
    plt.show()


if __name__ == "__main__":
    main()
