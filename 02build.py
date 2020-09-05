
import gzip
import glob
import os
import tarfile
import re

def read_clinical(filename):
    with tarfile.open(filename,"r:gz") as tar:
        for member in tar.getmembers():
            if member.name=="clinical.tsv":
                fp = tar.extractfile(member)
                b=fp.read()
                lines=b.decode("utf-8").split("\n")
                clin_mapping={}
                h=lines[0]
                header=h.strip().split("\t")
                #case_idx=header.index("case_id")
                case_idx=header.index("case_submitter_id")
                days_to_death_idx=header.index("days_to_death")
                days_to_last_follow_up_idx=header.index("days_to_last_follow_up")
                for line in lines[1:]:
                    arr=line.strip().split("\t")
                    if len(arr)>1:
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
                return clin_mapping

def read_mapping(filename):
    mapping={}
    #[uuid,sample["sample_id"],sample["submitter_id"]]
    for line in open(filename):
        arr=line.strip().split("\t")
        full_id=arr[2]
        if "-" in full_id:
            pos=full_id.rindex("-")
            full_id=full_id[:pos]
        mapping[arr[0]]=full_id
    return mapping

def get_id_data(basepath):
    #FPKM-UQ
    filelist = glob.glob(basepath+"/**/*.FPKM-UQ.txt.gz")
    print("filelist:",len(filelist))
    data=[]
    for filename in filelist:
        #print(filename)
        uuid = os.path.basename(os.path.dirname(filename))
        #print(uuid)
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
    return data

def get_id_data_ex(basepath,data):
    data_temp={}
    data_ex={}
    for vec in data:
        uuid=vec[0]
        case_id=vec[1]
        val=vec[2]
        filelist = glob.glob(basepath+"/"+uuid+"/*.FPKM-UQ.txt.gz")
        for filename in filelist:
            #print(filename)
            a={}
            with gzip.open(filename, 'rt') as fp:
                #file_content = f.read()
                for line in fp:
                    arr=line.strip().split("\t")
                    a[arr[0]]=arr[1]
            data_temp[case_id]=a
        data_ex[case_id]=val
    return data_ex,data_temp
 

for input_filename in glob.glob("data/*.id.txt"):
    m=re.match(r'data/(.*)\.id\.txt',input_filename)
    data_name=m.groups()[0]
    print(">>>",data_name)

    filename ="manifest/clinical.cases_selection.{}.tar.gz".format(data_name)
    clin_mapping=read_clinical(filename)
    print("clinical:  ",len(clin_mapping))
    filename="data/{}.id.txt".format(data_name)
    mapping=read_mapping(filename)
    print("id      :  ",len(mapping))

    base_path="data/{}".format(data_name)
    data=get_id_data(base_path)
    data_ex,data_temp=get_id_data_ex(base_path,data)

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

    output_filename="data/{}.data.tsv".format(data_name)
    print("[SAVE]",output_filename)
    fp=open(output_filename,"w")
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
        s=h+"\tgene_expression_FPKM-UQ\t"+"\t".join(val)+"\t"+"\t".join(v)
        fp.write(s)
        fp.write("\n")



