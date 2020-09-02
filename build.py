
import gzip
import glob
import os

mapping={}
#[uuid,sample["sample_id"],sample["submitter_id"]]
for line in open("id_mapping.txt"):
    arr=line.strip().split("\t")
    full_id=arr[2]
    if "-" in full_id:
        pos=full_id.rindex("-")
        full_id=full_id[:pos]
    mapping[arr[0]]=full_id
print("id_mapping.txt:",len(mapping))

clin_mapping={}
fp=open("clinical.tsv")
h=next(fp)
header=h.strip().split("\t")
#case_idx=header.index("case_id")
case_idx=header.index("case_submitter_id")
days_to_death_idx=header.index("days_to_death")
days_to_last_follow_up_idx=header.index("days_to_last_follow_up")
for line in fp:
    arr=line.strip().split("\t")
    cid=arr[case_idx]
    try:
        days_to_death=int(arr[days_to_death_idx])
    except:
        days_to_death=-1
    try:
        days_to_last_follow_up=int(arr[days_to_last_follow_up_idx])
    except:
        days_to_last_follow_up=-1
    clin_mapping[cid]=[str(days_to_death),str(days_to_last_follow_up)]
print("clinical.tsv:",len(clin_mapping))
print(clin_mapping)

filelist = glob.glob("**/*.FPKM.txt.gz")
print("filelist:",len(filelist))
data=[]
for filename in filelist:
    #print(filename)
    uuid = os.path.dirname(filename)
    if uuid in mapping:
        case_id=mapping[uuid]
        #print(uuid,"=>",case_id)
        if case_id in clin_mapping:
            val=clin_mapping[case_id]
            data.append([uuid,case_id,val])
        #else:
        #    print(">>>",case_id)
    #else:
    #    print(">>>")
print("#data:",len(data))
data_temp={}
data_ex={}
for vec in data:
    uuid=vec[0]
    case_id=vec[1]
    val=vec[2]
    filelist = glob.glob(uuid+"/*.FPKM.txt.gz")
    for filename in filelist:
        print(filename)
        a={}
        with gzip.open(filename, 'rt') as fp:
            #file_content = f.read()
            for line in fp:
                arr=line.strip().split("\t")
                a[arr[0]]=arr[1]
        data_temp[case_id]=a
    data_ex[case_id]=val
        
all_data={}
all_header=[]
all_keys=None
for h, obj in data_temp.items():
    all_header.append(h)
    for k,v in obj.items():
        if k not in all_data:
            all_data[k]=[]
        all_data[k].append(v)
    if all_keys is None:
       all_keys=list(all_data.keys())

fp=open("dataset.tsv","w")
s="\t".join(["sample_name","item_name","days_to_death","days_to_last_follow_up"])
# preprocessing ENSEMBL ID
all_keys_name=[]
for key in all_keys:
    k=key.split(".")[0]
    k="ENSEMBL:"+k
    all_keys_name.append(k)

fp.write(s+"\t"+"\t".join(all_keys_name))
fp.write("\n")
for i, h in enumerate(all_header):
    v=[all_data[k][i] for k in all_keys]
    val=data_ex[h]
    s=h+"\tgene_expression_FPKM\t"+"\t".join(val)+"\t"+"\t".join(v)
    fp.write(s)
    fp.write("\n")

"""
fp=open("dataset.tsv","w")
fp.write("gene\t"+"\t".join(all_header))
fp.write("\n")
for k in all_keys:
    v=all_data[k]
    s=k+"\t"+"\t".join(v)
    fp.write(s)
    fp.write("\n")
"""
