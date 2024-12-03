import os
import numpy as np
from PIL import Image
import argparse


# 读取npy转mask图像
def npy2mask(npypath, imgdir, suffix="png"):
    """
    :param npypath: npy文件地址
    :param imgdir: 图像存储文件夹地址
    :param suffix: 文件后缀
    :return: 正常执行返回0
    """
    img = Image.fromarray(np.load(npypath))
    fname = os.path.split(npypath)[-1].split('.')[0]
    img.convert("L").save(f"{imgdir}/{fname}.{suffix}")
    return 0


# 批量处理
def batch(npydir, imgdir, suffix="png"):
    if not os.path.exists(imgdir):
        os.mkdir(imgdir)
    for f in os.listdir(npydir):
        npy2mask(npypath=f"{npydir}/{f}",
                 imgdir=imgdir,
                 suffix=suffix)
    return 0


if __name__ == "__main__":
    print("npy可视化工具：读取矩阵并转化为8位黑白图像。")
    parser = argparse.ArgumentParser(description="将npy文件可视化为mask图像，默认为8位256黑白图像")
    parser.add_argument("--batch", "-b", action="store_true", help="处理目录下的所有npy文件")
    parser.add_argument("--create_folder", "-c", action="store_true", default=True, help="创建一个存储截屏的文件夹")
    parser.add_argument("--suffix", "-s", type=str, default="png", help="输出图像格式，默认为png格式")

    args = parser.parse_args()

    # 批量处理
    if args.batch:
        input_folder = input("输入待处理npy文件所在目录: ")
        output_folder = input("输入导出图片的输出目录: ")
        input_folder = input_folder.replace('\\', '/').replace("\"", "")
        output_folder = output_folder.replace('\\', '/').replace("\"", "")
        # 函数内置了新建文件夹功能
        if args.create_folder:
            output_folder = os.path.join(output_folder, "VisualSegmentationClass")
        batch(input_folder, output_folder, suffix=args.suffix)
    # 单文件处理
    else:
        input_file = input("输入待处理npy文件地址: ")
        output_file = input("输入导出图片的输出目录: ")
        input_directory = input_file.replace('\\', '/').replace("\"", "")
        output_directory = output_file.replace('\\', '/').replace("\"", "")
        npy2mask(input_directory, output_directory, suffix=args.suffix)

    input("处理完毕，任意键退出")
