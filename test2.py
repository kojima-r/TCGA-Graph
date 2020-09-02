#import pydot
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
import scipy as sp
from sklearn.covariance import GraphicalLasso
import  sklearn

def lasso_without_i(X,i,y,alpha):
    model=sklearn.linear_model.Lasso(alpha=alpha)
    x1=X[:,:i]
    x2=X[:,i+1:]
    xx=np.hstack((x1,x2))
    model.fit(xx,y)
    r2=model.score(xx,y)
    return model,xx,r2


alpha=1.0
#data = pd.read_csv("test_gene.csv")
#x=data.iloc[:,26:]
#y=data["GRADE_TYPE_x"]
data = pd.read_csv("dataset.tsv",sep='\t')
x=data.iloc[:,4:]
X=x.to_numpy()
print(X.shape)
n=X.shape[0] #サンプル数
nvar=X.shape[1] #変数の数(ノード数)

def process(i):
    result={}
    model,xx,r2=lasso_without_i(X,i,X[:,i],alpha)
    idx=np.where(model.coef_>1.0e-10)[0]
    result["model"]=model
    result["r2"]=r2
    result["target"]=i
    result["selected"]=idx
    result["subresults"]=[]
    #print(i,model.coef_)
    print(i,r2,len(idx),idx)
    for j in idx:
        model,xx,r2=lasso_without_i(xx,j,X[:,i],alpha)
        idx=np.where(model.coef_>1.0e-10)[0]
        subresult={}
        subresult["model"]=model
        subresult["r2"]=r2
        subresult["expand"]=j
        subresult["selected"]=idx
        result["subresults"].append(subresult)
    return result

from multiprocessing import Pool
p = Pool(64)
results=p.map(process, list(range(nvar)))
p.close()

import pickle
with open("result_tcga."+str(alpha)+".pkl", 'wb') as fp:
    pickle.dump(results,fp)

