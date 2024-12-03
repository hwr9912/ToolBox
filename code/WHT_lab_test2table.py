import re
import os
import csv
import json
import argparse
from tqdm import tqdm


def single(input_path, output_path):
    # 原始文本内容
    with open(input_path, "r", encoding="utf-8") as fin:
        text = fin.read()

    # 识别日期分割检查项目
    pattern = r"\d{4}-\d{2}-\d{2}:"
    dates = [i.replace(":", "") for i in re.findall(pattern, text)]
    # 识别分割符分割检查条目
    tests = [re.split(r",\s", t) for t in re.split(pattern, text)[1:]]
    # 定义一个正则表达式来匹配条目中的检查项目名称、检查结果、结果单位和正常值
    pattern = r"(\S+)\s{0,1}([\S]{1,})\s{0,1}(\S{0,})\s{0,1}([^\(\s]*)\({0,1}([^\s\)]*)\){0,1}\n{0,1}"
    results = []
    for test in tests:
        programs = []
        for program in test:
            try:
                name, value, unit, trend, normal = re.findall(pattern, program)[0]
                programs.append({
                    'program': name,
                    'value': value,
                    'unit': unit,
                    'trend': trend,
                    'normal': normal
                })
            except:
                print("未成功识别：", program)
        results.append(programs)
    # 汇总处理后数据
    lab_tests = {i: {"date": dates[i], "result": results[i]} for i in range(len(dates))}

    # 创建写模式，每个病人作为表格单独保存
    if output_path.endswith("json"):
        with open(output_path, "w") as fout:
            fout.write(json.dumps(lab_tests, indent=4, ensure_ascii=False))
    # 创建写模式，每个病人作为表格单独保存
    elif output_path.endswith("csv"):
        # 追加写模式，添加病人代号列
        if os.path.exists(output_path):
            patient = os.path.split(input_path)[-1].split(".")[0]
            # 打开一个CSV文件用于写入
            with open(output_path, 'a', newline='', encoding='utf-8') as csvfile:
                # 创建CSV写入器
                csvwriter = csv.writer(csvfile)

                # 遍历JSON数据并写入CSV
                for key, value in lab_tests.items():
                    date = value['date']
                    results = value['result']
                    for result in results:
                        csvwriter.writerow(
                            [patient, key, date, result['program'], result['value'], result['unit'], result['trend'],
                             result['normal']])
        else:
            # 打开一个CSV文件用于写入
            with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
                # 创建CSV写入器
                csvwriter = csv.writer(csvfile)

                # 写入表头
                csvwriter.writerow(['test', 'date', 'program', 'value', 'unit', 'trend', 'normal'])

                # 遍历JSON数据并写入CSV
                for key, value in lab_tests.items():
                    date = value['date']
                    results = value['result']
                    for result in results:
                        csvwriter.writerow(
                            [key, date, result['program'], result['value'], result['unit'], result['trend'],
                             result['normal']])
    else:
        print(f"请检查文件后缀名：{output_path}！")


def batch(input_directory,
          output_directory,
          args=None):
    if args.multiple_file:
        for f in tqdm(os.listdir(input_directory)):
            single(input_path=f"{input_directory}/{f}",
                   output_path=f"{output_directory}/{f.replace('txt', 'csv')}")
        return 0

    else:
        with open(f"{output_directory}/{args.filename}.csv", "w", newline='') as csvfile:
            # 创建CSV写入器
            csvwriter = csv.writer(csvfile)
            # 写入表头
            csvwriter.writerow(['patient', 'test', 'date', 'program', 'value', 'unit', 'trend', 'normal'])
        # 逐文件追加
        for f in tqdm(os.listdir(input_directory)):
            single(input_path=f"{input_directory}/{f}",
                   output_path=f"{output_directory}/{args.filename}.csv")
        return 0

def parse_args(text):
    print("██╗    ██╗██╗  ██╗████████╗ ██████╗  ██████╗ ██╗     \n"
          "██║    ██║██║  ██║╚══██╔══╝██╔═══██╗██╔═══██╗██║     \n"
          "██║ █╗ ██║███████║   ██║   ██║   ██║██║   ██║██║     \n"
          "██║███╗██║██╔══██║   ██║   ██║   ██║██║   ██║██║     \n"
          "╚███╔███╔╝██║  ██║   ██║   ╚██████╔╝╚██████╔╝███████╗\n"
          " ╚══╝╚══╝ ╚═╝  ╚═╝   ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝\n")
    print(f"本程序用于{text}")
    parser = argparse.ArgumentParser(description="从视频中提取每一帧作为图像并输出")
    parser.add_argument("--single", "-s", action="store_true", default=False,
                        help="处理单个文件，默认为批处理模式")
    parser.add_argument("--multiple_file", "-m", action="store_true", default=False,
                        help="每个检验文件单独保存为多个表格，表格名称为原文件名")
    parser.add_argument("--filename", "-fn", type=str, default="lab_test_results",
                        help="提供文件名，默认为lab_test_results，同时提供该项和multiple_file参数时，优先执行multiple_file模式")

    args = parser.parse_args()

    return args


if __name__ == "__main__":
    args = parse_args("给出检验结果文件地址(不能包含中文)，默认为批处理后存储为单个文件。")
    
    if args.single:
        input_path = input("输入待处理txt文件的地址: ")
        output_directory = input("输入导出结果文件的输出目录: ")
        input_path = input_path.replace('\\', '/').replace("\"", "")
        output_directory = output_directory.replace('\\', '/').replace("\"", "")
        name = os.path.split(input_path)[-1].split(".")[0]
        single(input_path=input_path,
               output_path=f"{output_directory}/{name}.csv")
    else:
        input_directory = input("输入所有待处理文件的输入目录: ")
        output_directory = input("输入导出表格的输出目录: ")
        input_directory = input_directory.replace('\\', '/').replace("\"", "")
        output_directory = output_directory.replace('\\', '/').replace("\"", "")
        batch(input_directory=input_directory,
              output_directory=output_directory,
              args=args)
        