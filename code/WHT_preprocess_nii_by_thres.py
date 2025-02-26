# conda activate base
# conda remove --name pack --all --keep-env
# conda install python pyinstaller tqdm numpy
# conda install simpleitk -c conda-forge
# pyinstaller -F D:\ToolBox\code\WHT_preprocess_nii_by_thres.py
# nuitka --standalone --onefile D:\ToolBox\code\WHT_preprocess_nii_by_thres.py --windows-icon-from-ico=D:\ToolBox\code\icon-console.ico
import os
import argparse
import numpy as np
from tqdm import tqdm
import SimpleITK as sitk


# 单文件模式
def single(image_path, save_path, args):
    """
    单个文件阈值分割
    :param image_path: 图像路径
    :param save_path: 处理后图像保存路径
    :param args: 命令行传参
    :return: 无返回，结果直接保存
    """
    image = sitk.ReadImage(image_path)
    matrix = sitk.GetArrayFromImage(image)
    if args.upper < matrix.max():
        matrix[matrix > args.upper] = args.upper
    if args.lower > matrix.min():
        matrix[matrix < args.lower] = args.lower
    result = sitk.GetImageFromArray(matrix)
    result.SetOrigin(image.GetOrigin())  # 恢复原始大小
    result.SetSpacing(image.GetSpacing())
    result.SetDirection(image.GetDirection())
    sitk.WriteImage(result, save_path)

# 表格匹配模式
def batch(images_root, save_dir, args):
    """
    多个文件阈值分割
    :param images_root: 图像路径
    :param save_dir: 处理后图像保存路径
    :param args: 命令行传参
    :return: 无返回，结果直接保存
    """
    for i in tqdm(os.listdir(images_root)):
        try:
            single(image_path=f"{images_root}/{i}",
                   save_path=f"{save_dir}/{i}",
                   args=args)
        except:
            print(f"文件{i}处理出现错误！")

def parse_args(text):
    print("██╗    ██╗██╗  ██╗████████╗ ██████╗  ██████╗ ██╗     \n"
          "██║    ██║██║  ██║╚══██╔══╝██╔═══██╗██╔═══██╗██║     \n"
          "██║ █╗ ██║███████║   ██║   ██║   ██║██║   ██║██║     \n"
          "██║███╗██║██╔══██║   ██║   ██║   ██║██║   ██║██║     \n"
          "╚███╔███╔╝██║  ██║   ██║   ╚██████╔╝╚██████╔╝███████╗\n"
          " ╚══╝╚══╝ ╚═╝  ╚═╝   ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝\n")
    print(f"欢迎使用WeHasTool. 我们将尝试{text}")
    parser = argparse.ArgumentParser(description="对目录下或单个的nifti格式数据进行阈值操作")
    parser.add_argument("--single", "-s", action="store_true", default=False,
                        help="单文件模式，该模式下仅处理单个文件。默认为批处理模式")
    parser.add_argument("--upper", "-u", type=np.float16, default=np.inf,
                        help="像素值上界，超出上界的像素赋值为上界")
    parser.add_argument("--lower", "-l", type=np.float16, default=-np.inf,
                        help="像素值下界，低于下界的像素赋值为下界")
    args = parser.parse_args()

    return args


if __name__ == "__main__":
    args = parse_args("对目录下或单个的nifti格式数据进行阈值操作，超出阈值上下限的均赋值为上下界")

    # 单文件模式
    if args.single:
        input_path = input("请输入单个待处理nii文件地址：").replace('\\', '/').replace("\"", "")
        output_path = input("请输入处理后nii文件保存目录：").replace('\\', '/').replace("\"", "")
        single(image_path=input_path,
               save_path=f"{output_path}/{os.path.split(input_path)[1]}",
               args=args)
    else:
        input_path = input("请输入所有待处理nii文件所在目录：").replace('\\', '/').replace("\"", "")
        output_path = input("请输入处理后nii文件保存目录：").replace('\\', '/').replace("\"", "")
        batch(images_root=input_path,
              save_dir=output_path,
              args=args)

    input("处理完毕，任意键退出...")
