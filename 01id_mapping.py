import requests
import json
import glob
import re
for filename in glob.glob("manifest/gdc_manifest.*.txt"):
    print(filename)
    fp= open(filename)
    m=re.match(r'manifest/gdc_manifest\.(.*)\.txt',filename)
    name=m.groups()[0]
    next(fp)
    uuids=[]
    for r in fp:
        arr=r.strip().split("\t")
        sid=arr[0]
        uuids.append(sid)
    #print(uuids)
    ofp= open("data/"+name+".id.txt","w")
    for uuid in uuids:
        url = 'https://api.gdc.cancer.gov/files/{:s}?expand=cases.samples&pretty=true'.format(uuid)
        print(url)
        response = requests.get(url)
        print(response)
        obj=json.loads(response.text)
        for case in obj["data"]["cases"]:
            for sample in case["samples"]:
                r=[uuid,sample["sample_id"],sample["submitter_id"]]
                ofp.write("\t".join(r))
                ofp.write("\n")
