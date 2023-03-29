import os

# 普通log信息，
class Log:
    def __init__(self):
        path = os.path.dirname(__file__)
        ppath = os.path.dirname(path)
        xpath = os.path.join(ppath, "files\\log.txt")
        self.f = open(xpath, 'w', encoding='utf-8')

    def log(self, string, *var):
        for v in var:
            string = string.replace('%s', str(v), 1)
        self.f.write(string)

# 交易详情
class TradeInfo:
    def __init__(self):
        path = os.path.dirname(__file__)
        ppath = os.path.dirname(path)
        xpath = os.path.join(ppath, "files\\trade_info.txt")
        self.f = open(xpath, 'w', encoding='utf-8')

    def log(self, string, *var):
        for v in var:
            string = string.replace('%s', str(v), 1)
        self.f.write(string)

# 每日持仓日志
class PositionInfo:
    def __init__(self):
        path = os.path.dirname(__file__)
        ppath = os.path.dirname(path)
        xpath = os.path.join(ppath, "files\\position.txt")
        self.f = open(xpath, 'w', encoding='utf-8')

    def log(self, string, *var):
        for v in var:
            string = string.replace('%s', str(v), 1)
        self.f.write(string)