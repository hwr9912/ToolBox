import os
from tqdm import tqdm
import nibabel as nib
import numpy as np
from scipy.ndimage import zoom
import argparse


def resize_nii(input_file, output_file, args):
    # 加载 NIfTI 文件
    nii_img = nib.load(input_file)
    img_data = nii_img.get_fdata()

    # 获取原始仿射矩阵
    original_affine = nii_img.affine

    # 计算新的图像尺寸
    new_shape = tuple(np.array(img_data.shape) * args.zoom_factor)

    # 使用 scipy.ndimage.zoom 进行图像缩放
    # order=3 代表三次样条插值
    # order=1 代表线性插值
    resized_data = zoom(img_data, zoom=(args.zoom_factor, args.zoom_factor, 1), order=1)

    if not args.image:
        resized_data = np.float64(resized_data > 0.5)

    # 创建新的 NIfTI 图像
    if args.renew_affline:
        # 更新仿射矩阵
        new_affine = original_affine.copy()
        new_affine[:3, :3] /= args.zoom_factor
        new_nii_img = nib.Nifti1Image(resized_data, affine=new_affine)
    else:
        new_nii_img = nib.Nifti1Image(resized_data, affine=original_affine)

    # 保存缩放后的 NIfTI 文件
    nib.save(new_nii_img, output_file)


def batch(input_directory, output_directory, args):
    count = 0
    for f in tqdm(os.listdir(input_directory)):
        try:
            resize_nii(input_file=f"{input_directory}/{f}",
                       output_file=f"{output_directory}/{f}",
                       args=args)
        except:
            print(f"{f}无法处理！")
            count += 1
    print(f"共处理了{len(os.listdir(input_directory))}个文件，其中{count}个无法处理！")


def parse_args(text):
    print("██╗    ██╗██╗  ██╗████████╗ ██████╗  ██████╗ ██╗     \n"
          "██║    ██║██║  ██║╚══██╔══╝██╔═══██╗██╔═══██╗██║     \n"
          "██║ █╗ ██║███████║   ██║   ██║   ██║██║   ██║██║     \n"
          "██║███╗██║██╔══██║   ██║   ██║   ██║██║   ██║██║     \n"
          "╚███╔███╔╝██║  ██║   ██║   ╚██████╔╝╚██████╔╝███████╗\n"
          " ╚══╝╚══╝ ╚═╝  ╚═╝   ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝\n")
    print(f"本程序用于{text}")
    parser = argparse.ArgumentParser(
        description="对目录下所有nii文件进行缩放处理，默认为缩小至0.25倍，文件类型为非image，不更新仿射矩阵")
    parser.add_argument("--zoom_factor", "-z", type=int, default=0.25,
                        help="缩放倍数，默认为0.25")
    parser.add_argument("--renew_affline", "-r", action="store_true", default=False,
                        help="更新仿射矩阵，默认为不更新")
    parser.add_argument("--image", "-i", action="store_true", default=False,
                        help="image模式，默认为mask模式")
    parser.add_argument("--single", "-s", action="store_true", default=False,
                        help="单文件模式， 默认为False")
    args = parser.parse_args()

    return args

if __name__ == "__main__":
    args = parse_args("nii文件缩放")
    if args.single:
        input_file = input("输入待处理文件：").replace('\\', '/').replace("\"", "")
        output_directory = input("输入处理后文件保存位置：").replace('\\', '/').replace("\"", "")
        name = os.path.split(input_file)[-1]
        resize_nii(input_file=input_file,
                   output_file=f"{output_directory}/{name}",
                   args=args)
    else:
        input_directory = input("输入待处理文件所在目录：").replace('\\', '/').replace("\"", "")
        output_directory = input("输入处理后文件保存位置：").replace('\\', '/').replace("\"", "")
        batch(input_directory=input_directory,
              output_directory=output_directory,
              args=args)

    input("处理完毕，任意键退出...")
