# nuitka --standalone --onefile D:\ToolBox\code\WHT_copy_folder_by_table.py --windows-icon-from-ico=.\code\icon-console.ico
# "E:\Anaconda_envs\envs\pack\Lib\site-packages\PyInstaller\bootloader\images\icon-console.ico"
# "F:\Electronic_Health_Image\computer_science_202411\dicom_series"
# "D:\Python\computer_vision\SRGAN\data\test.txt"
# "D:\Python\computer_vision\SRGAN\data\test"
import argparse
import os
import shutil
from tqdm import tqdm


def single(root, table, dest, args):
    # 创建路径
    os.makedirs(dest, exist_ok=True)
    # 读取列表
    with open(table, "r") as f:
        list = f.read().split("\n")
    # 生成绝对路径列表
    copy_dirs_set = {os.path.join(root, i).replace(os.sep, "/") for i in filter(None, list)}
    # 如果需要重命名
    if args.rename:
        # 遍历文件树
        with tqdm(total=len(copy_dirs_set)) as pbar:
            for crt_path, dirs, files in tqdm(os.walk(root)):
                # 取目录下文件名和需复制文件名交集和差集
                exist_absolute_dirs = set([os.path.join(crt_path, folder).replace(os.sep, "/") for folder in dirs]) & copy_dirs_set
                # 更新文件名列表
                copy_dirs_set = copy_dirs_set - exist_absolute_dirs
                # 提取父文件夹名称
                father_folder_name = os.path.split(crt_path)[-1]
                for folder in exist_absolute_dirs:
                    folder_name = os.path.split(folder)[-1]
                    # 复制文件
                    shutil.copytree(folder, f"{dest}/{father_folder_name}_{folder_name}")
                    pbar.update(1)
                # 判断集合copy_dirs_set是否为空
                if not copy_dirs_set:
                    return 0
    else:
        # 遍历文件树
        with tqdm(total=len(copy_dirs_set)) as pbar:
            for crt_path, dirs, files in os.walk(root):
                # 取目录下文件名和需复制文件名交集和差集
                exist_absolute_dirs = set(
                    [os.path.join(crt_path, folder).replace(os.sep, "/") for folder in dirs]) & copy_dirs_set
                # 更新文件名列表
                copy_dirs_set = copy_dirs_set - exist_absolute_dirs
                # 提取父文件夹名称
                father_folder_name = os.path.split(crt_path)[-1]
                for folder in exist_absolute_dirs:
                    folder_name = os.path.split(folder)[-1]
                    # 复制文件
                    shutil.copytree(folder, f"{dest}/{folder_name}")
                    pbar.update(1)
                # 判断集合copy_dirs_set是否为空
                if not copy_dirs_set:
                    return 0
    # 如果集合非空且要求输出总结文件
    if copy_dirs_set is not [] and args.summary:
        summary_path = os.path.split(dest)[0]
        print(f"一共有{len(copy_dirs_set)}个文件未找到！")
        with open(f"{summary_path}/{args.name}.csv", "w") as f:
            f.write("\n".join(copy_dirs_set)+"\n")


def parse_args(text):
    print("██╗    ██╗██╗  ██╗████████╗ ██████╗  ██████╗ ██╗     \n"
          "██║    ██║██║  ██║╚══██╔══╝██╔═══██╗██╔═══██╗██║     \n"
          "██║ █╗ ██║███████║   ██║   ██║   ██║██║   ██║██║     \n"
          "██║███╗██║██╔══██║   ██║   ██║   ██║██║   ██║██║     \n"
          "╚███╔███╔╝██║  ██║   ██║   ╚██████╔╝╚██████╔╝███████╗\n"
          " ╚══╝╚══╝ ╚═╝  ╚═╝   ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝\n")
    print(f"欢迎使用WeHasTool. 我们将尝试{text}")
    parser = argparse.ArgumentParser(
        description="按给定列表给出的文件夹名在指定目录下寻找文件夹，并将匹配到的文件夹复制到指定路径")
    parser.add_argument("--summary", "-s", action="store_true", default=False,
                        help="是否输出结果文件夹名列表（包含所有未匹配到的文件名，文件名以回车符分隔），默认为否")
    parser.add_argument("--name", "-n", type=str, default="summary",
                        help="输出结果列表的csv文件夹名（不含后缀），默认为summary")
    parser.add_argument("--rename", "-r", action="store_true", default=False,
                        help="是否将文件夹名改成 上级文件夹_原名 的格式，默认为否")

    opt = parser.parse_args()

    return opt


if __name__ == "__main__":
    args = parse_args("按给定列表给出的文件名在指定目录下寻找文件，并将匹配到的文件复制到指定路径。列表文件内容txt格式，文件名之间"
                      "以回车符分割")

    input_path = input("请输入待搜索父目录：").replace(os.sep, "/").replace("\"", "")
    input_table = input("请输入待匹配文件夹名列表：").replace(os.sep, "/").replace("\"", "")
    output_path = input("请输入您的输出目录：").replace(os.sep, "/").replace("\"", "")
    single(root=input_path,
           table=input_table,
           dest=output_path,
           args=args)

    input("处理完毕，任意键退出...")
