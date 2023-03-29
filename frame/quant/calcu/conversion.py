"""
数据处理函数
"""

# 导入机器学习的模块
from sklearn.linear_model import LinearRegression
import numpy as np

# 分位数取极值
def quantile(factor, up, down):
    up_scale = np.percentile(factor, up)
    down_scale = np.percentile(factor, down)
    factor = np.where(factor > up_scale, up_scale, factor)
    factor = np.where(factor < down_scale, down_scale, factor)
    return factor

# 3倍数中位数绝对偏差去极值
def med(factor):
    median = np.median(factor)

    #求出每个因子值与中位数的绝对偏差值,而后求出该中位数
    me = np.median(abs(factor - median))

    med_e = 3 * 1.4826 * me

    up = median + med_e
    down = median - med_e

    factor = np.where(factor > up, up, factor)
    factor = np.where(factor < down, down, factor)
    return factor

# 3sigma方法去极值
def threesigma(factor):
    mean = factor.mean()
    std = factor.std()

    up = mean + 3 * std
    down = mean - 3 * std

    factor = np.where(factor > up, up, factor)
    factor = np.where(factor < down, down, factor)

    return factor

# 标准化
def standardlize(factor):  #标准化处理
    mean = factor.mean()
    std = factor.std()

    return (factor - mean) / std

# 中性化
def neutralize(factor, target, feature):                                          #中性化。去除因子和市值之间的联系
    factor[target] = med(factor[target])                 #去极值
    factor[target] = standardlize(factor[target])        #标准化
    x = factor[feature].reshape(-1, 1)                       #x为市值，将其固定为1列
    y = factor[target]                                       #因子数据

    #建立回归方程并预测
    lr = LinearRegression()         #y = wx + b
    lr.fit(x, y)
    y_predict = lr.predict(x)

    #去除线性关系
    factor[target] = y - y_predict
