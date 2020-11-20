import pandas as pd
import numpy as np
filename="data/ovary.2020-09-02.data.tsv"
data = pd.read_csv(filename,sep='\t')
x=data.iloc[:,4:]
X=x.to_numpy()
n=X.shape[0] #サンプル数
nvar=X.shape[1] #変数の数(ノード数)
print("[LOAD]",filename,":",X.shape)

m=np.mean(X[:,0])
s=np.std(X[:,0])
print("0:{:02.2}\t{:02.2}".format(m,s))

