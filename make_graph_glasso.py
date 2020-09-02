#import pydot
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
import scipy as sp
from sklearn.covariance import GraphicalLasso
import pickle

#X:データ, alpha:L1正則化パラメータ, disp_heatmap:結果を表示するかどうか
def Graphical_Lasso(X, alpha, disp_heatmap=True):
    #データの正規化（必須）
    X=sp.stats.zscore(X,axis=0)
     
    #GraphLasso
    print("==")
    model = GraphicalLasso(alpha=alpha,verbose=True)
    print("==")
    model.fit(X)
    print("==")
     
    cov_ = model.covariance_ #スパース化した分散共分散行列
    pre_ = model.precision_ #スパース化した分散共分散行列の逆行列
     
    #分散共分散行列のヒートマップによる表示
    if disp_heatmap==True:
        f, axes = plt.subplots(1, 3, figsize=(15, 4))
        axes[0].set_title('Sample covariance')
        axes[1].set_title('Estimated covariance')
        axes[2].set_title('Estimated precision')
         
        #sns.heatmap(cov, ax=axes[0])
        sns.heatmap(cov_, ax=axes[1])
        sns.heatmap(pre_, ax=axes[2])
        plt.savefig("a.png")
    return model
def Compute_extended_BIC(model,n,p,gamma):
    omega = model.precision_
    cov = model.covariance_
    E=(np.sum(np.sum(omega != 0, axis=0))-p)*0.5
    #尤度
    MLE=n*(np.log(np.linalg.det(omega))-np.trace(np.dot(cov,omega)))
     
    EBIC=-MLE+E*np.log(n)+4*E*gamma*np.log(p)
    return EBIC

#data = pd.read_csv("test_gene.csv")
from sklearn import preprocessing
le = preprocessing.LabelEncoder()
data = pd.read_csv("single_kidney_genedata.csv")
x=data.iloc[:,26:]
y=le.fit_transform(data["GRADE_TYPE_x"])
#import sklearn
#import sklearn.covariance
#sklearn.__version__
#cov=np.cov(x.T) #標本分散共分散行列
#print(cov.shape)
#A=sklearn.covariance.graphical_lasso(cov,alpha=0.5)
#print(A)
X=x.to_numpy()
Y=y
print(X.shape)
n=X.shape[0] #サンプル数
p=X.shape[1] #変数の数(ノード数)
from sklearn.feature_selection import SelectKBest, f_regression
selector = SelectKBest(score_func=f_regression, k=1000) 
selector.fit(X, Y)
mask = selector.get_support() 
X_selected = selector.transform(X)



#Graphical Lassoの実行
alpha=0.7 #L1正則化パラメータ
model=Graphical_Lasso(X_selected, alpha)
with open("model."+str(alpha)+".pkl", 'wb') as fp:
    pickle.dump(model,fp)
#BIC, EBICの計算
BIC=Compute_extended_BIC(model,n,p,0)
print("BIC  :"+str(BIC)+" alpha :"+str(alpha))
EBIC=Compute_extended_BIC(model,n,p,0.5)
print("EBIC :"+str(EBIC)+" alpha :"+str(alpha))
    
