# conda activate base
# conda remove --name pack --all --keep-env
# conda install python pyinstaller tqdm
# pyinstaller -F .\code\WHT_rename_file_by_table.py
import argparse
from tqdm import tqdm
import os
import csv

# 表格匹配模式
def batch(root, table, args):
    try:
        # 构建匹配字典
        match_dict = {}
        with open(table, mode='r', newline='', encoding='gbk') as file:
            for row in csv.reader(file):
                match_dict[row[0]] = row[1]
        # 未匹配计数
        count = 0
        # 全文件树搜索模式
        if args.all:
            with tqdm(total=len(match_dict)) as pbar:
                for crt_path, dirs, files in os.walk(root):
                    # 对目录下文件名列表和匹配列表
                    for f in set(files)-set(match_dict.values()):
                        os.rename(f"{crt_path}/{f}", f"{crt_path}/{match_dict[f]}")
                        # 用后即弃
                        match_dict.pop(f)
                        pbar.update(1)
                    # 如果匹配字典为空则退出
                    if len(match_dict) == 0: break
                for key in match_dict:
                    pbar.update(1)
                    count += 1
                    if not args.simple: print(f"文件{key}不在目录下！")
                print(
                    f"表格中的{len(match_dict)}个文件中，共计重命名了{len(match_dict) - count}个文件，{count}个文件未能匹配。")
        # 第一级目录搜索模式
        else:
            # 遍历匹配字典
            for key in tqdm(match_dict):
                try:
                    os.rename(f"{root}/{key}", f"{root}/{match_dict[key]}")
                except:
                    count += 1
                    if not args.simple: print(f"文件{key}不在目录下！")
        # 处理总结
        print(f"表格中的{len(match_dict)}个文件中，共计重命名了{len(match_dict)-count}个文件，{count}个文件未能匹配。")
    except:
        print("请检查文件格式!")

def parse_args(text):
    print("██╗    ██╗██╗  ██╗████████╗ ██████╗  ██████╗ ██╗     \n"
          "██║    ██║██║  ██║╚══██╔══╝██╔═══██╗██╔═══██╗██║     \n"
          "██║ █╗ ██║███████║   ██║   ██║   ██║██║   ██║██║     \n"
          "██║███╗██║██╔══██║   ██║   ██║   ██║██║   ██║██║     \n"
          "╚███╔███╔╝██║  ██║   ██║   ╚██████╔╝╚██████╔╝███████╗\n"
          " ╚══╝╚══╝ ╚═╝  ╚═╝   ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝\n")
    print(f"欢迎使用WeHasTool. 我们将尝试{text}")
    parser = argparse.ArgumentParser(
        description="按给定列表给出的文件名在指定目录下寻找文件，并将匹配到的文件重命名成对应的名称")
    # parser.add_argument("--table", "-t", action="store_true", default=False,
    #                     help="匹配依据改为表格模式，默认为正则模式。表格包含两列，第一列为原文件名称，第二列为修改后名称，两列均不包含路径，分隔符为逗号")
    parser.add_argument("--all", "-a", action="store_true", default=False,
                        help="全文件树搜索模式，默认为仅在第一级目录搜索。该模式下将遍历并重命名父目录下的所有首次匹配的子文件")
    # parser.add_argument("--recycle", "-r", action="store_true", default=False,
    #                     help="（仅适用于全文件树搜索+表格重命名模式）键值对匹配后仍然保留在匹配字典中，默认为用后即弃")
    parser.add_argument("--simple", "-s", action="store_true", default=False,
                        help="简略信息模式，默认为唠叨模式。该模式下不再展示未匹配的文件名")

    args = parser.parse_args()

    return args


if __name__ == "__main__":
    args = parse_args("按给定列表给出的文件名在指定目录下寻找文件，并将匹配到的文件重命名成对应的名称")

    # # 表格重命名模式
    # if args.table:
    input_path = input("请输入待重命名文件所在父目录：").replace('\\', '/').replace("\"", "")
    input_table = input("请输入待匹配文件名列表：").replace('\\', '/').replace("\"", "")
    batch(root=input_path,
          table=input_table,
          args=args)
    # # 正则表达式模式
    # else:
    #     input_path = input("请输入待重命名文件所在父目录：").replace('\\', '/').replace("\"", "")
    #     input_regex = input("请输入待匹配正则表达式：")
    #     batch_regex(root=input_path,
    #                 regex=input_regex,
    #                 args=args)

    input("处理完毕，任意键退出...")
