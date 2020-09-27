#import pydot
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
import scipy as sp
from sklearn.covariance import GraphicalLasso
import  sklearn
from sklearn.preprocessing import StandardScaler

from multiprocessing import Pool
import pickle

import argparse
import os

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

parser = argparse.ArgumentParser()
parser.add_argument('-a', '--alpha', type=float, default=0.1) 
parser.add_argument('-f', '--filename', type=str, default="data/ovary.2020-09-02.data.tsv")
parser.add_argument('-o', '--output', type=str, default="result")
parser.add_argument('-r', '--rank', type=int, default=0) 
parser.add_argument('-l', '--limit_len', type=int, default=0) 
args = parser.parse_args()

alpha=args.alpha
filename=args.filename
data = pd.read_csv(filename,sep='\t')
x=data.iloc[:,4:]
X=x.to_numpy()
n=X.shape[0]
nvar=X.shape[1]
print("[LOAD]",filename,":",X.shape)
sc = StandardScaler()
X = sc.fit_transform(X)
os.makedirs(args.output,exist_ok=True)
def process(i):
    result={}
    model,w,b,x_next,r2=lasso_without_i(X,i,X[:,i],alpha)
    idx=np.where(model.coef_>1.0e-10)[0]
    #result["model"]=model
    result["w"]=w[idx]
    result["b"]=b
    result["r2"]=r2
    result["target"]=i
    result["selected"]=idx
    if args.rank>0:
        candidate=sorted(zip(w[idx],idx),reverse=True,key=lambda x:np.abs(x[0]))
        result["subresults"]=[]
        if args.limit_len>0:
            next_idx=[]
            for x in candidate[:args.limit_len]:
                if x[1]>=i:
                    next_idx.append(x[1]-1)
                else:
                    next_idx.append(x[1])
        else:
            next_idx=[]
            for x in candidate:
                if x[1]>=i:
                    next_idx.append(x[1]-1)
                else:
                    next_idx.append(x[1])
        for j in next_idx:
            model,w,b,x_next2,r2=lasso_without_i(x_next,j,X[:,i],alpha)
            idx=np.where(model.coef_>1.0e-10)[0]
            subresult={}
            subresult["w"]=w[idx]
            subresult["b"]=b
            subresult["r2"]=r2
            subresult["expand"]=j
            subresult["selected"]=idx
            result["subresults"].append(subresult)
    return result

p = Pool(32)
results=p.map(process, list(range(nvar))[:1])
p.close()

name, _ = os.path.splitext( os.path.basename(filename) )
output_path=args.output+"/"+name+".result."+str(alpha)+".pkl"
with open(output_path, 'wb') as fp:
    pickle.dump(results,fp)
output_path=args.output+"/"+name+".scale."+str(alpha)+".pkl"
with open(output_path, 'wb') as fp:
    pickle.dump(sc,fp)

