import re
import os

def extract_signals(verilog_file, output_file):
    # 定义匹配 wire 和 reg 的正则表达式
    signal_pattern = re.compile(r'\b(wire|reg)\b\s*(\[[^\]]+\])?\s*([\w, ]+)(;|=)')
    
    extracted_signals = []
    
    # 读取 sv 文件内容
    with open(verilog_file, 'r') as file:
        lines = file.readlines()
    
    # 逐行解析
    for line in lines:
        match = signal_pattern.search(line)
        if match:
            signal_type = match.group(1)  # wire or reg
            width = match.group(2) if match.group(2) else ""  # [8:0] or empty
            names = match.group(3)  # 信号名
            # 分解信号名并格式化
            if signal_type == "reg":
                signal_type = "logic"
            if width=="" :
                for name in names.split(','):
                    extracted_signals.append(f"  - \"{signal_type} {name.strip()}\"")
            else :
                for name in names.split(','):
                    extracted_signals.append(f"  - \"{signal_type} {width.strip()} {name.strip()}\"")
    
    # 写入到 yaml 文件
    basename = os.path.basename(verilog_file)
    filename = os.path.splitext(basename)[0]
    with open(output_file, 'w') as file:
        file.write(filename + ':\n')
        for signal in extracted_signals:
            file.write(signal + '\n')

# 使用示例
verilog_file = '../../../../rtl/rtl/LoadQueueRAR.sv'  # 输入的 sv 文件
output_file = 'internal.yaml'  # 输出的 yaml 文件

extract_signals(verilog_file, output_file)
