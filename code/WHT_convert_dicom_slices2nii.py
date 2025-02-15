# pyinstaller -F --hiddenimport=pydicom.encoders.gdcm --hiddenimport=pydicom.encoders.pylibjpeg code\WHT_convert_dicom_slices2nii.py
import argparse
import os
import SimpleITK as sitk
from tqdm import tqdm


def single(dicom_slices, output_file):
    image_file_reader = sitk.ImageFileReader()
    # 读取DICOM序列
    image_file_reader.SetImageIO("GDCMImageIO")
    image_file_reader.SetFileName(dicom_slices)
    image_file_reader.ReadImageInformation()
    # 同步像素尺寸
    image_size = list(image_file_reader.GetSize())
    if len(image_size) == 3 and image_size[2] == 1:
        image_size[2] = 0
    image_file_reader.SetExtractSize(image_size)
    image = image_file_reader.Execute()
    # 将DICOM图像转换为Nifti格式
    image_array = sitk.GetArrayFromImage(image)  # 将SimpleITK图像转换为NumPy数组
    image_out = sitk.GetImageFromArray(image_array)  # 将NumPy数组转换回SimpleITK图像
    image_out.SetOrigin(image.GetOrigin())  # 恢复原始大小
    image_out.SetSpacing(image.GetSpacing())
    image_out.SetDirection(image.GetDirection())
    sitk.WriteImage(image_out, output_file)

def batch(input_directory, output_directory):
    for f in tqdm(os.listdir(input_directory)):
        try:
            single(dicom_slices=f"{input_directory}/{f}",
                   output_file=f"{output_directory}/{f.replace(".dcm", "")}.nii")
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
        description="打包指定目录下的所有dicom单张图片文件为nii.gz，默认为批处理模式，默认输出目录不新建文件夹")
    parser.add_argument("--create_folder", "-c", nargs="?", const="1xnii", type=str, default=None,
                        help="输出目录下新建输出文件夹，默认为不更新")
    parser.add_argument("--single", "-s", action="store_true", default=False,
                        help="单文件模式， 默认为False")
    args = parser.parse_args()

    return args


if __name__ == "__main__":
    args = parse_args("打包指定目录下的所有dicom文件到nii，并且将子目录名作为打包文件名，并保持目录结构，"
                      "等转化完后检查输出目录是否符合预期。")
    # 单文件模式
    if args.single:
        input_path = input("请输入您的单个待转化dicom序列：").replace('\\', '/').replace("\"", "")
        output_path = input("请输入您的输出目录：").replace('\\', '/').replace("\"", "")
        if args.create_folder is not None:
            output_path = f"{output_path}/{args.create_folder}"
            os.mkdir(output_path)
        name = os.path.split(input_path)[-1].replace(".dcm", "")
        single(dicom_slices=input_path,
               output_file=f"{output_path}/{name}.nii.gz")
    # 批处理模式
    else:
        input_path = input("请输入您的待转化dicom文件所在目录：").replace('\\', '/').replace("\"", "")
        output_path = input("请输入您的输出目录：").replace('\\', '/').replace("\"", "")
        if args.create_folder is not None:
            output_path = f"{output_path}/{args.create_folder}"
            os.mkdir(output_path)
        batch(input_directory=input_path,
              output_directory=output_path)

    input("处理完毕，任意键退出...")
