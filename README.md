# TCGA-Graph
- https://portal.gdc.cancer.gov/
RNA-seq, HTSeq-FPKM-UQ, txt

##  Data dowonload
```
wget https://gdc.cancer.gov/files/public/file/gdc-client_v1.6.0_Ubuntu_x64-py3.7_0.zip
unzip gdc-client_v1.6.0_Ubuntu_x64-py3.7_0.zip 
```
##  Data preprocess

```
./gdc-client download -m gdc_manifest.2020-08-25.txt 
python id_mapping.py
python build.py
```
wget https://repo.anaconda.com/archive/Anaconda3-2020.07-Linux-x86_64.sh
