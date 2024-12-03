# pyinstaller -F D:\ToolBox\comp\WHT_copy_file_by_table.py
import argparse
import os
import shutil
from tqdm import tqdm


def single(root, table, dest, args):
    # 读取列表
    with open(table, "r") as f:
        list = f.read().split("\n")
    copy_files_set = {i for i in filter(None, list)}
    # 遍历文件树
    with tqdm(total=len(copy_files_set)) as pbar:
        for crt_path, dirs, files in tqdm(os.walk(root)):
            # 取列表交集和差集
            exist_files = set(files) & copy_files_set
            copy_files_set = copy_files_set - exist_files
            for file in exist_files:
                # 复制文件
                shutil.copy(os.path.join(crt_path, file), dest)
                pbar.update(1)
            # 判断集合copy_files_set是否为空
            if not copy_files_set:
                return 0
    if copy_files_set is not [] and args.result:
        result_path = os.path.split(dest)[0]
        with open(f"{result_path}/{args.name}.csv", "w") as f:
            f.write("\n".join(copy_files_set)+"\n")


def parse_args(text):
    print("██╗    ██╗██╗  ██╗████████╗ ██████╗  ██████╗ ██╗     \n"
          "██║    ██║██║  ██║╚══██╔══╝██╔═══██╗██╔═══██╗██║     \n"
          "██║ █╗ ██║███████║   ██║   ██║   ██║██║   ██║██║     \n"
          "██║███╗██║██╔══██║   ██║   ██║   ██║██║   ██║██║     \n"
          "╚███╔███╔╝██║  ██║   ██║   ╚██████╔╝╚██████╔╝███████╗\n"
          " ╚══╝╚══╝ ╚═╝  ╚═╝   ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝\n")
    print(f"欢迎使用WeHasTool. 我们将尝试{text}")
    parser = argparse.ArgumentParser(
        description="按给定列表给出的文件名在指定目录下寻找文件，并将匹配到的文件复制到指定路径")
    parser.add_argument("--result", "-r", action="store_true", default=False,
                        help="是否输出结果文件名列表（包含所有未匹配到的文件名，文件名以回车符分隔），默认为否")
    parser.add_argument("--name", "-n", type=str, default="result",
                        help="输出结果列表的csv文件名（不含后缀），默认为result")
    args = parser.parse_args()

    return args


if __name__ == "__main__":
    args = parse_args("按给定列表给出的文件名在指定目录下寻找文件，并将匹配到的文件复制到指定路径。列表文件内容txt格式，文件名之间"
                      "以回车符分割")

    input_path = input("请输入待搜索父目录：").replace('\\', '/').replace("\"", "")
    input_table = input("请输入待匹配文件名列表：").replace('\\', '/').replace("\"", "")
    output_path = input("请输入您的输出目录：").replace('\\', '/').replace("\"", "")
    single(root=input_path,
           table=input_table,
           dest=output_path,
           args=args)

    input("处理完毕，任意键退出...")
