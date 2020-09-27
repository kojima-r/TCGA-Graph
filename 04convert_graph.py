import pickle
import numpy as np
import pandas as pd
alpha=0.1
#alpha=10.0

filename="data/ovary.2020-09-02.data.tsv"
with open(filename) as fp:
    h=next(fp)
    arr=h.split("\t")
    head_arr=arr[4:]
#filename="data/ovary.2020-09-02.data.tsv"
#data = pd.read_csv(filename,sep='\t')
#x=data.iloc[:,0]
histo_in_degree=[]
histo_out_degree=[]
histo_in_w=[]
histo_r2=[]
counter_out_degree={}
with open("result_tcga."+str(alpha)+".pkl", 'rb') as fp:
    res=pickle.load(fp)
    for r in res:
        target=r["target"]
        n=np.sum(r["w"]>0.00002)
        #histo_in_degree.append(len(r["selected"]))
        histo_in_degree.append(n)
        histo_r2.append(r["r2"])
        histo_in_w.extend(r["w"])
        for idx in r["selected"]:
            ## histogram of out-degree
            if idx>=target:
                selected_idx=idx+1
            else:
                selected_idx=idx
            if selected_idx not in counter_out_degree:
                counter_out_degree[selected_idx]=0
            counter_out_degree[selected_idx]+=1

for k,v in counter_out_degree.items():
    histo_out_degree.append(v)
import matplotlib.pyplot as plt

fig = plt.figure()
plt.hist(histo_in_w, bins=50,range=(0,10.0))
plt.yscale('log')
fig.savefig("histo_in_w.png")
plt.clf()

fig = plt.figure()
plt.hist(histo_in_degree, bins=50)
fig.savefig("histo_in.png")
plt.clf()

fig = plt.figure()
plt.hist(histo_out_degree, bins=50)
fig.savefig("histo_out.png")
plt.clf()

fig = plt.figure()
plt.hist(histo_r2, bins=50, range=(-0.1,1.0))
fig.savefig("histo_r2.png")
plt.clf()

### output ===
ofp=open("result_tcga."+str(alpha)+".tsv", 'w')
with open("result_tcga."+str(alpha)+".pkl", 'rb') as fp:
    res=pickle.load(fp)
    for r in res:
        target=r["target"]
        r2=r["r2"]
        w0=r["b"]
        rank=0
        #print(r["w"])
        for i, idx in enumerate(r["selected"]):
            ## histogram of out-degree
            if idx>=target:
                selected_idx=idx+1
            else:
                selected_idx=idx
            #print(target,"lasso",selected_idx,r["w"][i])
            el1=head_arr[target]
            el2=head_arr[selected_idx]
            arr=[el1,"lasso",el2,rank,r["w"][i],w0,r2]
            s="\t".join(map(str,arr))
            ofp.write(s)
            ofp.write("\n")


