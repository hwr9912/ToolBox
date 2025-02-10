# pyinstaller -F D:\ToolBox\code\WHT_compress_tiff.py
import os
import tifffile as tif
import argparse
from tqdm import tqdm
import imagecodecs._imcd

def single(image_path:str=None,
           save_dir:str=None,
           compression:str="LZW",
           dpi:int=300,
           **kwargs):
    img = tif.imread(image_path)
    fname = os.path.split(image_path)[-1]
    tif.imwrite(f"{save_dir}/{fname}", img, compression=compression, resolution=(dpi, dpi), **kwargs)

def batch(input_directory, output_directory, **kwargs):
    for f in tqdm(os.listdir(input_directory)):
        single(f"{input_directory}/{f}", output_directory, **kwargs)

def parse_args(text):
    print("██╗    ██╗██╗  ██╗████████╗ ██████╗  ██████╗ ██╗     \n"
          "██║    ██║██║  ██║╚══██╔══╝██╔═══██╗██╔═══██╗██║     \n"
          "██║ █╗ ██║███████║   ██║   ██║   ██║██║   ██║██║     \n"
          "██║███╗██║██╔══██║   ██║   ██║   ██║██║   ██║██║     \n"
          "╚███╔███╔╝██║  ██║   ██║   ╚██████╔╝╚██████╔╝███████╗\n"
          " ╚══╝╚══╝ ╚═╝  ╚═╝   ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝\n")
    print(f"欢迎使用WeHasTool. 我们将尝试{text}")
    parser = argparse.ArgumentParser(
        description="压缩所有目录下的tif/tiff文件的体积，默认为批处理模式, 压缩模式包含:"
                    "1. LZW（默认）:compression='LZW'"
                    "2. zlib: compression='zlib', compressionargs={'level': 8}"
                    "3. jpeg: compression='jpeg'")
    parser.add_argument("--single", "-s", action="store_true", default=False,
                        help="单文件模式， 默认为False")
    # parser.add_argument("--single", "-s", action="store_true", default=False,
    #                     help="单文件模式， 默认为False")
    args = parser.parse_args()

    return args


if __name__ == "__main__":
    args = parse_args("压缩所有目录下的tif/tiff文件的体积，默认为批处理模式。")
    # 单文件模式
    if args.single:
        input_path = input("请输入您的单个待压缩tiff图片目录：").replace('\\', '/').replace("\"", "")
        output_path = input("请输入您的输出目录：").replace('\\', '/').replace("\"", "")
        name = os.path.split(input_path)[-1]
        single(image_path=input_path, save_dir=output_path)
    # 批处理模式
    else:
        input_path = input("请输入您的待压缩tiff图片目录：").replace('\\', '/').replace("\"", "")
        output_path = input("请输入您的输出目录：").replace('\\', '/').replace("\"", "")
        batch(input_directory=input_path,
              output_directory=output_path)

    input("处理完毕，任意键退出...")
