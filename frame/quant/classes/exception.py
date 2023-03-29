from quant.classes.object import *

def exceptional_handle(string):
    TradeInfo.f.close()
    PositionInfo.f.close()
    Log.f.close()
    raise Exception(string)