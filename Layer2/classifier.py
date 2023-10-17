import json

def descisionTree(u,nr_packets,c,nrPacketsMode,widthwave):
    if u == 1:
        return False
    else:
        if 25<c<50:
            return False
        elif c<25:
            if nr_packets<170:
                return False
            else:
                return True 
        else:
            if u/c > 0.9:
                return False
            else:
                if nrPacketsMode > 0.7:
                    return False
                else:
                    if 1<widthwave<50:
                        return True
                    else:
                        return False

with open("flow_data.json") as jsonFIle:
    flowData = json.load(jsonFIle)

for flow in flowData:
    src = flow["flow_id"][0]
    dst = flow["flow_id"][2]
    c = flow["c"]
    multimod = flow["multimod"]
    u = flow["unique"]
    nr_mode = flow["nrPacketsMode"]
    nr_packets = flow["nrPackets"]
    multimod2 = flow["multimod2"]
    widthwave = flow["widthave"]
    autocorr = flow["autocorr"]

    print(src,"\t-\t",dst,"\t\t",descisionTree(u,nr_packets,c,nr_mode,widthwave*1000))

