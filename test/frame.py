from overall import *

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime
from dateutil.parser import parse
import tushare as ts

from settingfunction import set_benckmark

def initialize(context):
    set_benckmark('000001.SZ')
    g.p1 = 5
    g.p2 = 60
    g.security = '000006.SZ'

def handle_data(context):
    hist = attribute_history(g.security, g.p2)
    ma5 = hist['close'][-g.p1].mean()
    ma60 = hist['close'].mean()

    if ma5 > ma60 and g.security not in context.positions:
        order_value(g.security, context.cash)
    elif ma5 < ma60 and g.security in context.positions:
        order_target(g.security, 0)
    