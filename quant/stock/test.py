from quant.classes.object import *
from quant.stock.get_fun import *

'''
这个文件用来测试get_fun写的函数
'''


#测试行    get_giant_list
# context.dt=pd.to_datetime('20190113',format='%Y%m%d')
# date = '2018-09-28'
# context.dt = parse(date)
# print(get_giant_list(1, ['002219.SZ']))

#测试行 history     attribute_history
context.dt=pd.to_datetime('20190113',format='%Y%m%d')
# print(attribute_history(20,'000001.SZ'))
# print(history(5,'1m','close',['000001.SZ','600000.SH','000300.XSHG'],True))
ddf = attribute_history(10,['000001.SZ'],unit='1m',fields=['open', 'close', 'high', 'low', 'vol'],isdf=True)
print(type(ddf['close']))