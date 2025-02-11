# pyinstaller -F D:\ToolBox\code\WHT_copy_file_by_table.py
# "E:\Anaconda_envs\envs\pack\Lib\site-packages\PyInstaller\bootloader\images\icon-console.ico"
import argparse
import os
import shutil
from tqdm import tqdm


def single(root, table, dest, args):
    # 读取列表
    with open(table, "r") as f:
        list = f.read().split("\n")
    copy_files_set = {i for i in filter(None, list)}
    # 如果需要重命名
    if args.rename:
        # 如果要求复制所有重名文件
        if args.duplicated:
            # 遍历文件树
            with tqdm(total=len(copy_files_set)) as pbar:
                for crt_path, dirs, files in tqdm(os.walk(root)):
                    # 取目录下文件名和需复制文件名交集和差集
                    exist_files = set(files) & copy_files_set
                    # 提取父文件夹名称
                    father_folder_name = os.path.split(crt_path)[-1]
                    for file in exist_files:
                        # 复制文件
                        shutil.copy(f"{crt_path}/{file}", f"{dest}/{father_folder_name}_{file}")
                        pbar.update(1)
                    # 不再判断集合copy_files_set是否为空，直接退出
        else:
            # 遍历文件树
            with tqdm(total=len(copy_files_set)) as pbar:
                for crt_path, dirs, files in tqdm(os.walk(root)):
                    # 取目录下文件名和需复制文件名交集和差集
                    exist_files = set(files) & copy_files_set
                    # 更新文件名列表
                    copy_files_set = copy_files_set - exist_files
                    # 提取父文件夹名称
                    father_folder_name = os.path.split(crt_path)[-1]
                    for file in exist_files:
                        # 复制文件
                        shutil.copy(f"{crt_path}/{file}", f"{dest}/{father_folder_name}_{file}")
                        pbar.update(1)
                    # 判断集合copy_files_set是否为空
                    if not copy_files_set:
                        return 0
    else:
        # 遍历文件树
        with tqdm(total=len(copy_files_set)) as pbar:
            for crt_path, dirs, files in tqdm(os.walk(root)):
                # 取目录下文件名和需复制文件名交集和差集
                exist_files = set(files) & copy_files_set
                copy_files_set = copy_files_set - exist_files
                for file in exist_files:
                    # 复制文件
                    shutil.copy(f"{crt_path}/{file}", f"{dest}/{file}")
                    pbar.update(1)
                # 判断集合copy_files_set是否为空
                if not copy_files_set:
                    return 0
    # 如果集合非空且要求输出总结文件
    if copy_files_set is not [] and args.summary and not args.duplicated:
        summary_path = os.path.split(dest)[0]
        print(f"一共有{len(copy_files_set)}个文件未找到！")
        with open(f"{summary_path}/{args.name}.csv", "w") as f:
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
    parser.add_argument("--summary", "-s", action="store_true", default=False,
                        help="是否输出结果文件名列表（包含所有未匹配到的文件名，文件名以回车符分隔），默认为否")
    parser.add_argument("--name", "-n", type=str, default="summary",
                        help="输出结果列表的csv文件名（不含后缀），默认为summary")
    parser.add_argument("--rename", "-r", action="store_true", default=False,
                        help="是否将文件名改成 上级文件夹_原名 的格式，默认为否")
    parser.add_argument("--duplicated", "-d", action="store_true", default=False,
                        help="是否允许同一文件名在不同路径下多次搜索，默认为否(危险操作，谨慎开启，开启后--rename设定为True)")
    args = parser.parse_args()

    if args.duplicated:
        args.rename = True

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
