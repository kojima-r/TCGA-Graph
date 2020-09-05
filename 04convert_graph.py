import pickle
import pandas as pd
alpha=1.0

#filename="data/ovary.2020-09-02.data.tsv"
#data = pd.read_csv(filename,sep='\t')
#x=data.iloc[:,0]
histo_in_degree=[]
histo_out_degree=[]
histo_in_w=[]
counter_out_degree={}
with open("result_tcga."+str(alpha)+".pkl", 'rb') as fp:
    res=pickle.load(fp)
    for r in res:
        target=r["target"]
        histo_in_degree.append(len(r["selected"]))
        for idx in r["selected"]:
            histo_in_w.append(r["w"][idx])
            if idx>=target:
                selected_idx=idx+1
            else:
                selected_idx=idx
            #selected.append(selected_idx)
            if selected_idx not in counter_out_degree:
                counter_out_degree[selected_idx]=0
            counter_out_degree[selected_idx]+=1
            #print(target,selected_idx)

for k,v in counter_out_degree.items():
    histo_out_degree.append(v)
import matplotlib.pyplot as plt

fig = plt.figure()
plt.hist(histo_in_w, bins=50)
fig.savefig("histo_in_w.png")
plt.clf()

fig = plt.figure()
plt.hist(histo_in_degree, bins=50)
fig.savefig("histo_in.png")
plt.clf()

fig = plt.figure()
plt.hist(histo_out_degree, bins=50)
fig.savefig("histo_out.png")

