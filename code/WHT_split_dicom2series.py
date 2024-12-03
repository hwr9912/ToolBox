# pyinstaller -F D:\ToolBox\comp\WHT_split_dicom2series.py
import argparse
import os
import shutil
import SimpleITK as sitk
# conda install simpleitk -c conda-forge
from tqdm import tqdm


def single(dicom_folder, output_folder, args):
    # 创建ImageSeriesReader对象
    reader = sitk.ImageSeriesReader()
    reader.LoadPrivateTagsOn()

    # 获取该文件夹下的所有系列ID
    series_ids = reader.GetGDCMSeriesIDs(dicom_folder)
    # 设置计数器
    count = 0

    # 遍历所有系列ID
    for idx, series_id in enumerate(series_ids):
        # 获取该 series 的所有文件名
        file_names = reader.GetGDCMSeriesFileNames(dicom_folder, series_id)

        # 检查文件数量
        if len(file_names) > args.begin and len(file_names) < args.end:
            # 迭代计数器
            count += 1
            # 设置文件名
            metadata = sitk.ImageFileReader()
            metadata.SetFileName(file_names[0])
            metadata.LoadPrivateTagsOn()
            metadata.ReadImageInformation()
            patient_id = metadata.GetMetaData("0010|0020").replace(' ','')

            # 为该 series 创建单独的输出文件夹
            output_series_directory = os.path.join(output_folder, f"{patient_id}_{idx}")
            os.makedirs(output_series_directory, exist_ok=True)

            # 按顺序编号从1开始复制文件
            for index, file_name in enumerate(file_names):
                shutil.copy(file_name, f"{output_series_directory}/{index}.dcm")

    if count == 0:
        print(f"{os.path.split(dicom_folder)[1]}中未找到对应dicom序列!")


def batch(input_directory, output_directory, args):
    for f in tqdm(os.listdir(input_directory)):
        try:
            single(dicom_folder=f"{input_directory}/{f}",
                   output_folder=output_directory,
                   args=args)
        except:
            print(f"{input_directory}/{f}处理失败！")


def parse_args(text):
    print("██╗    ██╗██╗  ██╗████████╗ ██████╗  ██████╗ ██╗     \n"
          "██║    ██║██║  ██║╚══██╔══╝██╔═══██╗██╔═══██╗██║     \n"
          "██║ █╗ ██║███████║   ██║   ██║   ██║██║   ██║██║     \n"
          "██║███╗██║██╔══██║   ██║   ██║   ██║██║   ██║██║     \n"
          "╚███╔███╔╝██║  ██║   ██║   ╚██████╔╝╚██████╔╝███████╗\n"
          " ╚══╝╚══╝ ╚═╝  ╚═╝   ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝\n")
    print(f"欢迎使用WeHasTool. 我们将尝试{text}")
    parser = argparse.ArgumentParser(
        description="切分指定目录下的所有dicom文件夹为dicom序列文件夹，默认为批处理模式，默认将新建文件夹，Patient ID作为打包文件名")
    parser.add_argument("--single", "-s", action="store_true", default=False,
                        help="单文件模式， 默认为False")
    parser.add_argument("--begin", "-b", type=int, default=90,
                        help="dicom序列包含文件的最小数目，默认为90，小于该值的序列不保存")
    parser.add_argument("--end", "-e", type=int, default=float("inf"),
                        help="dicom序列包含文件的最大数目，默认为正无穷，大于该值的序列不保存")
    args = parser.parse_args()

    return args


if __name__ == "__main__":
    args = parse_args("切分指定目录下的所有dicom文件夹到为dicom序列文件夹，并且将Patient ID作为打包文件名，并保持目录结构，"
                      "等转化完后检查输出目录是否符合预期。")
    # 单文件模式
    if args.single:
        input_path = input("请输入您的单个待转化dicom文件夹：").replace('\\', '/').replace("\"", "")
        output_path = input("请输入您的输出目录：").replace('\\', '/').replace("\"", "")
        single(dicom_folder=input_path,
               output_folder=output_path,
               args=args)
    # 批处理模式
    else:
        input_path = input("请输入您的待转化dicom文件夹所在目录：").replace('\\', '/').replace("\"", "")
        output_path = input("请输入您的输出目录：").replace('\\', '/').replace("\"", "")
        batch(input_directory=input_path,
              output_directory=output_path,
              args=args)

    input("处理完毕，任意键退出...")
