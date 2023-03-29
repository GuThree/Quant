# from .models import Code
import os
import sys
import json
import numpy as np
from django.http import HttpResponseRedirect
from django.shortcuts import render
import subprocess
from django.contrib import messages

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# coding=UTF-8
def frame(request):
    # 获取文件路径
    strategy_path = os.path.abspath('frame/strategy.py')
    log_path = os.path.abspath('frame/quant/files/log.txt')
    position_path = os.path.abspath('frame/quant/files/position.txt')
    tra_info_path = os.path.abspath('frame/quant/files/trade_info.txt')

    if request.method == 'POST':
        if 'run' in request.POST:
            frame_content = request.POST.get('user_post')  # user_post是name属性，为用户在页面上编写的策略部分
            frame_content = frame_content.replace('\r', '') # 去除传入内容中的'\r'
            # 将用户修改写入策略文件，with关键字会自动关闭，不用设置close
            with open(strategy_path, 'w', encoding="utf-8") as f:  # 以写的方式打开strategy.py文件
                f.write(frame_content)  # 将前端用户书写的策略代码写入strategy.py

            # 获取日期和金额
            d1 = request.POST.get("start_date")
            d2 = request.POST.get("end_date")
            d3 = request.POST.get("cash")
            result = subprocess.run(['python', 'frame/run.py', d1, d2, d3], capture_output=True)  # 运行run.py并获取输出值
            # print(result)
            result_str = result.stdout.decode().strip()  # 将结果字符串赋值给一个变量
            # print(result_str)
            result_list = result_str.split('\r\n')  # 将结果字符串拆分成列表
            # # 判断数据长度是否符合要求
            # if len(result_list) <= 17:
            #     messages.error(request, "运行失败！请检查网络或日期或策略！")
            #     os.system("git checkout frame/strategy.py")  # 暂时的解决方案: 将strategy.py恢复初始状态
            #     return HttpResponseRedirect('/frame')
            print(result_list)

            # ----------------------------结果字符串分割-------------------------
            trade_date = result_list[17].strip('[]').replace("\'", "").split(', ')
            ratio_list = result_list[18].strip('[]').replace("\'", "").split(', ')  # 去除字符串中的字符并分割
            ratio_list = list(map(float, ratio_list))  # 将列表中的字符串转为float型
            ratio_list = list(np.round_(np.array(ratio_list), 2))  # 将字符串中的数据保留2位小数
            benckmark_ratio_list = result_list[19].strip('[]').replace("\'", "").split(', ')
            benckmark_ratio_list = list(map(float, benckmark_ratio_list))
            benckmark_ratio_list = list(np.round_(np.array(benckmark_ratio_list), 2))
            # print(trade_date, type(trade_date))
            # print(ratio_list, type(ratio_list))
            # print(benckmark_ratio_list, type(benckmark_ratio_list))

            # -------------------读取文件，with关键字会自动关闭，不用设置close---------------------
            with open(strategy_path, 'r', encoding="utf-8") as f:
                frame_content = f.read()
            with open(log_path, 'r', encoding="utf-8") as f:
                log_info = f.read()
                log_info = log_info.split('\n')
                # print(log_info, type(log_info), len(log_info))
            with open(position_path, 'r', encoding="utf-8") as f:
                pos_info = f.read()
                pos_info = pos_info.split('\n')
            with open(tra_info_path, 'r', encoding="utf-8") as f:
                tra_info = f.read()
                tra_info = tra_info.split('\n')

            # -------------------传数据给前端---------------------
            return render(request, 'quantitative transaction.html', {
                "frame_content": frame_content,
                "log_info": log_info,
                "pos_info": pos_info,
                "tra_info": tra_info,
                "Total_Returns": result_list[0],
                "Total_Annualized_Returns": result_list[1],
                "Alpha": result_list[2],
                "Beta": result_list[3],
                "Sharpe": result_list[4],
                "Algorithm_Volatility": result_list[5],
                "Benchmark_Volatility": result_list[6],
                "Downside_Risk": result_list[7],
                "Sortino": result_list[8],
                "Information_Ratio": result_list[9],
                "profit_time": result_list[10],
                "loss_time": result_list[11],
                "winning": result_list[12],
                "winning_daily": result_list[13],
                "profit_loss_ratio": result_list[14],
                "Max_Drawdown_L": result_list[15],
                "Max_Drawdown_R": result_list[16],
                "trade_date": json.dumps(trade_date),
                "ratio_list": json.dumps(ratio_list),
                "benckmark_ratio_list": json.dumps(benckmark_ratio_list),
            })

    else:  # 初始时呈现给用户的界面
        os.system("git checkout frame/strategy.py") # 重新进入页面后将strategy.py恢复到初始状态

        with open(strategy_path, 'r', encoding="utf-8") as f:
            frame_content = f.read()
        with open(log_path, 'r+', encoding="utf-8") as f:
            f.truncate(0)
            log_info = f.read()
            log_info = log_info.split('\n')
            # print(log_info, type(log_info), len(log_info))
        with open(position_path, 'r+', encoding="utf-8") as f:
            f.truncate(0)
            pos_info = f.read()
            pos_info = pos_info.split('\n')
        with open(tra_info_path, 'r+', encoding="utf-8") as f:
            f.truncate(0)
            tra_info = f.read()
            tra_info = tra_info.split('\n')

        return render(request, 'quantitative transaction.html', {
            "frame_content": frame_content,
            "log_info": log_info,
            "pos_info": pos_info,
            "tra_info": tra_info,
            "Total_Returns": "--",
            "Total_Annualized_Returns": "--",
            "Alpha": "--",
            "Beta": "--",
            "Sharpe": "--",
            "Algorithm_Volatility": "--",
            "Benchmark_Volatility": "--",
            "Downside_Risk": "--",
            "Information_Ratio": "--",
            "Sortino": "--",
            "profit_loss_ratio": "--",
            "profit_time": "--",
            "loss_time": "--",
            "winning": "--",
            "winning_daily": "--",
            "Max_Drawdown_L": "----",
            "Max_Drawdown_R": "----",
            "trade_date": json.dumps(['2002-01-01', '2002-01-02', '2002-01-03', '2002-01-04', '2002-01-05']),
            "ratio_list": json.dumps([0, 0, 0, 0, 0]),
            "benckmark_ratio_list": json.dumps([0, 0, 0, 0, 0]),
        })
