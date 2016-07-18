import sys, os, urllib, urlparse, optparse, time
import numpy as np
import matplotlib.pyplot as plt

def DataDownload(remotedir, filename, localdir="./"):
    remoteaddr = 'http://%s%s' % (remotedir, filename)
    (scheme, server, path, params, query, frag) = urlparse.urlparse(remoteaddr)
    localname = os.path.split(path)[1]
    #print remoteaddr, localname
    try:
        # retrieve remoteaddr from server and store in localname on client
        urllib.urlretrieve(remoteaddr, localdir+localname+".txt")
    except IOError, e:
        print "ERROR: Failed to download. Error is: %s"% e.errno


def getObjectList(id, survey):
    if survey == "3pi":
        url = "http://star.pst.qub.ac.uk/sne/ps13pi/psdb/candidate/" + id + "/"
        servername = "star.pst.qub.ac.uk/sne/ps13pi/psdb/lightcurve/"
    elif survey == "md":
        url = "http://star.pst.qub.ac.uk/sne/ps1md/psdb/candidate/" + id + "/"
        servername = "star.pst.qub.ac.uk/sne/ps1md/psdb/lightcurve/"
    elif survey == "old_md":
        url = "http://star.pst.qub.ac.uk/ps1/psdb/candidate/" + id + "/"
        servername = "star.pst.qub.ac.uk/ps1/psdb/lightcurve/"
    print url
    html = urllib.urlopen(url).read()
    #print html
    index = html.index("Object List")
    objectList = html[index:index+50]
    if "good" in objectList:
        return "good"
    elif "garbage" in objectList:
        return "garbage"
    elif "confirmed" in objectList:
        return "confirmed"
    elif "possible" in objectList:
        return "possible"
    elif "attic" in objectList:
        return "attic"
    elif "zoo" in objectList:
        return "zoo"

def main():
    parser = optparse.OptionParser("[!] usage: python get_web_info.py\n"+\
                               "\t -F <data file>\n"+\
                               "\t -s <survey [3pi, md, old_md] >\n")
    
    parser.add_option("-F", dest="dataFile", type="string", \
                      help="specify data file to get web info for")
    parser.add_option("-s", dest="survey", type="string", \
                      help="specify which survey this is for [3pi, md, old_md]")
                      
    (options, args) = parser.parse_args()
    dataFile = options.dataFile
    survey = options.survey

    if dataFile == None or survey == None:
        print parser.usage
        exit(0)
    
    try:
        assert survey in set(["3pi", "md", "old_md"])
    except AssertionError:
        sys.exit("[!] survey must be one of [3pi, md, old_md]")

    lists = {
             "confirmed" : [],
             "good"      : [],
             "possible"  : [],
             "attic"     : [],
             "zoo"       : [],
             "garbage"   : []
            }
    """
    output_file = "web_info_%s.csv" % dataFile.split("/")[-1].split(".")[0]
    output = open(output_file,"w")

    ref = {}
    for line in open("web_info_classifications_by_object_20160709.csv","r").readlines():
        data = line.split(",")
        ref[data[0]] = data[1]

    for i,line in enumerate(open(dataFile,"r").readlines()):
        if "subject_id" in line:
            continue
        id = line.split(",")[0]
        try:
            list = ref[id]
        except KeyError:
            try:
                list = getObjectList(id, survey)
            except IOError:
                time.sleep(60)
                list = getObjectList(id, survey)
        lists[list].append(float(line.split(",")[1].strip()))
        output.write("%s,%s,%s\n"%(id,list,line.split(",")[1].strip()))
    output.close()
    """

    colourmap = {
                 "confirmed" : "#0014CE",
                 "possible"  : "#FCB606",
                 "good"      : "#F00200",
                 "attic"     : "#3D348B",
                 "zoo"       : "#011627",
                 "garbage"   : "#669D31"
                }

    p_real = {}
    for line in open(dataFile,"r").readlines():
        data = line.split(",")
        p_real[data[0]] = float(data[1])

    for line in open("web_info_classifications_by_object_20160711_sinceJun22.csv","r").readlines():
        data = line.split(",")
        #if data[1] == "good" and p_real[data[0]] < 0.5:
        #    print data[0]
        #lists[data[1]].append(float(data[2].strip()))
        lists[data[1]].append(p_real[data[0]])

    bins = [x for x in np.arange(0,1.02,0.02)]


    l = ["garbage","attic"]
    for key in l:
        try:
            counts, bins, patches = plt.hist(lists[key],bins=bins,label=key,color=colourmap[key],alpha=1)
        except IndexError:
            continue
        if key == "garbage":
            garbage_count = counts
        if key == "attic":
            attic_count = counts

    print attic_count, garbage_count
    print list(np.where(np.array(attic_count) < np.array(garbage_count))[0])
    try:
        overlap = list(np.where(np.array(garbage_count) < np.array(attic_count))[0])
        for i in range(len(overlap)):
            to_plot = [bins[overlap[i]], bins[overlap[i]+1]]
            plt.hist(lists["garbage"],bins=to_plot,color=colourmap["garbage"],alpha=1)
    except IndexError:
        pass
    """
    try:
        overlap = list(np.where(np.array(garbage_count) <= np.array(attic_count))[0])
        for i in range(len(overlap)):
            to_plot = [bins[overlap[i]], bins[overlap[i]+1]]
            plt.hist(lists["garbage"],bins=bins,color=colourmap["garbage"],alpha=1)
    except IndexError:
        pass
    """
    l = ["zoo", "possible", "good"]
    for key in l:
        try:
            counts, bins, patches = plt.hist(lists[key],bins=bins,label=key,color=colourmap[key],alpha=1)
        except IndexError:
            continue

    #plt.plot([0.436,0.436],[0,80],"k--",lw=2)
    plt.xlabel("P(real)")
    plt.ylabel("frequency")
    plt.legend()
    #plt.show()
    plt.savefig("aggregated_by_PS1_object_%s.pdf"%dataFile.split(".")[0],bbox_inches="tight")

if __name__ == "__main__":
    main()
