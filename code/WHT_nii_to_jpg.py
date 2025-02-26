# pyinstaller -F D:\ToolBox\code\WHT_nii_to_jpg.py
import os
import argparse
import numpy as np
from tqdm import tqdm
import SimpleITK as sitk
from PIL import Image


def nii_to_jpg(image_path, save_path, args):
    """
    将单个 NIfTI 文件转换为 JPG 图片
    :param image_path: NIfTI 文件路径
    :param save_path: 输出 JPG 图片目录
    :param args: 命令行参数
    :return: 无返回，结果直接保存
    """
    image = sitk.ReadImage(image_path)
    matrix = sitk.GetArrayFromImage(image)
    if len(matrix.shape) == 2:
        matrix = np.expand_dims(matrix, axis=2)

    # 获取图片切片大小
    if args.axis == "coronal":
        slices = matrix.shape[0]
    elif args.axis == "sagittal":
        slices = matrix.shape[1]
    elif args.axis == "axial":
        slices = matrix.shape[2]
    else:
        raise ValueError("无效的轴向: 只能是 'coronal', 'sagittal' 或 'axial'")

    # 创建输出目录
    os.makedirs(save_path, exist_ok=True)

    for i in range(slices):
        # 获取切片
        if args.axis == "coronal":
            slice_data = matrix[i, :, :]
        elif args.axis == "sagittal":
            slice_data = matrix[:, i, :]
        elif args.axis == "axial":
            slice_data = matrix[:, :, i]

        # 归一化像素值到 0-255
        slice_data = (slice_data - np.min(slice_data)) / (np.max(slice_data) - np.min(slice_data)) * 255
        slice_data = slice_data.astype(np.uint8)

        # 转换为 PIL 图像并保存为 JPG
        rgb_image = np.stack((slice_data,) * 3, axis=-1)
        img = Image.fromarray(rgb_image)

        img.save(os.path.join(save_path, f"{os.path.basename(image_path).split(".")[0]}_{args.axis}_{i}.jpg"))


def batch_nii_to_jpg(input_dir, output_dir, args):
    """
    批量处理 NIfTI 文件转换为 JPG
    :param input_dir: 输入 NIfTI 文件目录
    :param output_dir: 输出 JPG 文件目录
    :param axis: 切片轴（coronal, sagittal, axial）
    :param args: 命令行参数
    :return: 无返回，结果直接保存
    """
    for file_name in tqdm(os.listdir(input_dir), desc="Processing all files"):
        if file_name.endswith((".nii", ".nii.gz")):
            try:
                nii_to_jpg(image_path=os.path.join(input_dir, file_name), save_path=output_dir, args=args)
            except Exception as e:
                print(f"文件 {file_name} 处理失败: {e}")


def parse_args(description_text):
    print("██╗    ██╗██╗  ██╗████████╗ ██████╗  ██████╗ ██╗     \n"
          "██║    ██║██║  ██║╚══██╔══╝██╔═══██╗██╔═══██╗██║     \n"
          "██║ █╗ ██║███████║   ██║   ██║   ██║██║   ██║██║     \n"
          "██║███╗██║██╔══██║   ██║   ██║   ██║██║   ██║██║     \n"
          "╚███╔███╔╝██║  ██║   ██║   ╚██████╔╝╚██████╔╝███████╗\n"
          " ╚══╝╚══╝ ╚═╝  ╚═╝   ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝\n")
    print(f"欢迎使用WeHasTool. 我们将尝试 {description_text}")
    parser = argparse.ArgumentParser(description="将单个或多个 NIfTI 格式文件转换为 JPG 图片")
    parser.add_argument("--single", "-s", action="store_true", default=False,
                        help="单文件模式，该模式下仅处理单个文件。默认为批处理模式")
    parser.add_argument("--axis", "-a", choices=["coronal", "sagittal", "axial"], default="axial",
                        help="从 3D 体数据保存图片的轴向（coronal, sagittal 或 axial，默认是 axial）")
    args = parser.parse_args()

    return args


def main():
    description = "将单个或多个 NIfTI 格式文件转换为 JPG 图片"
    args = parse_args(description_text=description)

    # 单文件模式
    if args.single:
        input_path = input("请输入单个待处理 NIfTI 文件地址：").replace('\\', '/').replace("\"", "")
        output_path = input("请输入 JPG 图片保存目录：").replace('\\', '/').replace("\"", "")
        nii_to_jpg(image_path=input_path, save_path=output_path, args=args)
    else:
        input_dir = input("请输入所有待处理 NIfTI 文件所在目录：").replace('\\', '/').replace("\"", "")
        output_dir = input("请输入 JPG 图片保存目录：").replace('\\', '/').replace("\"", "")
        batch_nii_to_jpg(input_dir=input_dir, output_dir=output_dir, args=args)

    print("处理完成！")


if __name__ == "__main__":
    main()
