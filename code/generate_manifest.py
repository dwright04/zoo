import os, optparse

import numpy as np

def main():

    parser = optparse.OptionParser("[!] usage: python generate_manifest.py\n"+\
                                   "           -l <log file>\n"+\
                                   "           -L <limit number of subjects in each partition (default=500)>"
                                  )

    parser.add_option("-l", dest="log_file", type="string", \
                      help="specify the log file containg the images to be added to the manifest")
    parser.add_option("-L", dest="limit", type="float", \
                      help="specify a limit to the number of subjects to be included in each manifest")

    (options, args) = parser.parse_args()

    try:
        log_file = options.log_file
        limit    = options.limit
    except (TypeError, AttributeError), e:
        print e
        print parser.usage
        exit(0)

    if log_file is None:
        print parser.usage
        exit(0)
    if limit is None:
        limit = 500.0

    image_map = {}

    for line in open(log_file,"r").readlines():
        file = line.strip()
        triple_id = file.split("_")[0] + "_" + file.split("_")[1] + "_" + file.split("_")[2] + "_" + file.split("_")[3]
        try:
            for key in image_map[triple_id].keys():
                if key in file:
                    image_map[triple_id][key] = file
        except KeyError:
            image_map[triple_id]  = {"id":file.split("_")[0],"target":None,"ref":None,"diff":None}
            for key in image_map[triple_id].keys():
                if key in file:
                    image_map[triple_id][key] = file

    del_counter = 0
    for k in image_map.keys():
        for key in image_map[k].keys():
            try:
                if image_map[k][key] is None:
                    del_counter += 1
                    del image_map[k]
            except KeyError:
                continue
    print del_counter

    tot_subjects = len(image_map.keys())

    number_partitions = int(np.ceil(tot_subjects / limit))

    mjd = log_file.split("/")[0]
    path = log_file.split("/")[0] + "/" + log_file.split("/")[1] + "/" + log_file.split("/")[2]   
    counter = 0
    for i in range(1,number_partitions+1):

        os.mkdir(path+"/"+str(i))
        output = open("%s/%d/%s_part%d_manifest.csv"%(path,i,mjd,i),"w")
        output.write("#object_id,#image_group_id,target,ref,diff\n")
 
        for key in image_map.keys()[counter:]:
            output.write("#%s,#%s,%s,%s,%s\n"%(image_map[key]["id"],\
                                               key,\
                                               image_map[key]["target"],\
                                               image_map[key]["ref"],\
                                               image_map[key]["diff"]
                                              )
                        )
            print path+"/"+image_map[key]["target"], path+"/"+str(i)+"/"+image_map[key]["target"]
            os.rename(path+"/"+image_map[key]["target"], path+"/"+str(i)+"/"+image_map[key]["target"])
            os.rename(path+"/"+image_map[key]["ref"], path+"/"+str(i)+"/"+image_map[key]["ref"])
            os.rename(path+"/"+image_map[key]["diff"], path+"/"+str(i)+"/"+image_map[key]["diff"])
            counter += 1
            if counter % limit == 0:
                print counter
                break
        output.close()

if __name__ == "__main__":
    main()
