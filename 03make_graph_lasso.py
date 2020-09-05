#import pydot
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
import scipy as sp
from sklearn.covariance import GraphicalLasso
import  sklearn

from multiprocessing import Pool
import pickle

def lasso_without_i(X,i,y,alpha):
    model=sklearn.linear_model.Lasso(alpha=alpha)
    x1=X[:,:i]
    x2=X[:,i+1:]
    xx=np.hstack((x1,x2))
    model.fit(xx,y)
    r2=model.score(xx,y)
    w=model.coef_
    b=model.intercept_
    #
    return model,w,b,xx,r2


alpha=1.0
filename="data/ovary.2020-09-02.data.tsv"
data = pd.read_csv(filename,sep='\t')
x=data.iloc[:,4:]
X=x.to_numpy()
n=X.shape[0] #サンプル数
nvar=X.shape[1] #変数の数(ノード数)
print("[LOAD]",filename,":",X.shape)

def process(i):
    result={}
    model,w,b,xx,r2=lasso_without_i(X,i,X[:,i],alpha)
    idx=np.where(model.coef_>1.0e-10)[0]
    #result["model"]=model
    result["w"]=w
    result["b"]=b
    result["r2"]=r2
    result["target"]=i
    result["selected"]=idx
    print(">>",i)
    if False:
        result["subresults"]=[]
        #print(i,model.coef_)
        print(i,r2,len(idx),idx)
        for j in idx:
            model,w,b,xx,r2=lasso_without_i(xx,j,X[:,i],alpha)
            idx=np.where(model.coef_>1.0e-10)[0]
            subresult={}
            subresult["model"]=model
            subresult["w"]=w
            subresult["b"]=b
            subresult["r2"]=r2
            subresult["expand"]=j
            subresult["selected"]=idx
            result["subresults"].append(subresult)
    return result

p = Pool(90)
results=p.map(process, list(range(nvar)))
p.close()

with open("result_tcga."+str(alpha)+".pkl", 'wb') as fp:
    pickle.dump(results,fp)

