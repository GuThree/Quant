"""
数据处理函数
"""

#导入机器学习的模块
from sklearn.linear_model import LinearRegression


#去极值
def de_extremum(factor):  #中位数绝对偏差法去极值
    median = np.median(factor)  #求出中位数

    #求出每个因子值与中位数的绝对偏差值,而后求出该中位数
    mad=np.median(abs(factor-median))

    #求出参数mad_e,参数n取3
    mad_e=3*1.4826*mad

    #求出上下限：
    up=median + mad_e
    down=median - mad_e

    #去极值
    factor=np.where(factor>up,up,factor)
    factor=np.where(factor<down,down,factor)
    return factor #返回去极值后的因子

#标准化
def standardlize(factor):  #标准化处理
    mean=factor.mean()
    std=factor.std

    return (factor-mean)/std

#中性化
def neutralize(factor):   #中性化。去除因子和市值之间的联系
    factor['pb_ratio']=de_extremum(factor['pb_ratio'])  #去极值
    factor['pb_ratio']=stand(factor['pb_ratio'])  #标准化
    x=factor['market_cap'].reshape(-1,1)   #x为市值，将其固定为1列
    y=factor['pb_ratio']   #因子数据

    #建立回归方程并预测
    lr=LinearRegression()   #y=wx+b
    lr.fit(x,y)
    y_predict=lr.predict(x)

    #去除线性关系
    factor['pb_ratio']=y-y_predict
