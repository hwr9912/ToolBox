import argparse
import os
from typing import Tuple, Any

import cv2
from tqdm import tqdm


def single(input_path: str,
           output_path: str,
           fps: int = 15,
           fourcc: str = "XVID",
           resolution: tuple[int, int] = (640, 480)):
    # 读取视频
    capture = cv2.VideoCapture(input_path)
    # 输出视频
    writer = cv2.VideoWriter(output_path,
                             fourcc=cv2.VideoWriter.fourcc(*fourcc),
                             fps=fps,
                             frameSize=resolution)
    while True:
        ret, frame = capture.read()
        if not ret:
            break

        # 调整视频帧的分辨率
        resized_frame = cv2.resize(frame, resolution)

        # 将帧写入输出视频
        writer.write(resized_frame)
    capture.release()
    writer.release()
    return 0


def batch(input_directory: str,
          output_directory: str,
          fps: int = 15,
          fourcc: str = "XVID",
          resolution: tuple[int, int] = (640, 480)):
    error_count = 0
    for f in tqdm(os.listdir(input_directory)):
        try:
            single(input_path=f"{input_directory}/{f}",
                   output_path=f"{output_directory}/{f.replace("mp4", "avi")}",
                   fps=fps,
                   fourcc=fourcc,
                   resolution=resolution)
        except:
            error_count += 1
            print(f"{f}处理失败!")
    print(f"共处理了{len(os.listdir(input_directory))}个文件，{error_count}个文件处理失败。")
    return 0


def parse_args(text):
    print("██╗    ██╗██╗  ██╗████████╗ ██████╗  ██████╗ ██╗     \n"
          "██║    ██║██║  ██║╚══██╔══╝██╔═══██╗██╔═══██╗██║     \n"
          "██║ █╗ ██║███████║   ██║   ██║   ██║██║   ██║██║     \n"
          "██║███╗██║██╔══██║   ██║   ██║   ██║██║   ██║██║     \n"
          "╚███╔███╔╝██║  ██║   ██║   ╚██████╔╝╚██████╔╝███████╗\n"
          " ╚══╝╚══╝ ╚═╝  ╚═╝   ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝\n")
    print(f"欢迎使用WeHasTool. 我们将尝试{text}")
    parser = argparse.ArgumentParser(description=f"本脚本程序目标为{text}")
    # 用户没有提供 -c 或 --create_folder选项时，create_folder的值为None。
    # 用户提供了 -c 或 --create_folder但没有指定值时，create_folder的值为"video"。
    # 用户提供了 -c 或 --create_folder并指定了值时，create_folder的值为用户指定的字符串。
    parser.add_argument("--create_folder", "-c", nargs="?", const="video", type=str, default=None,
                        help="输出目录下新建输出文件夹，默认为不更新")
    parser.add_argument("--single", "-s", action="store_true", default=False,
                        help="单文件模式， 默认为False")
    parser.add_argument("--frame_per_sec", "-f", type=int, default=15,
                        help="帧数，默认为15fps")
    parser.add_argument("--resolution", "-r", type=str, default="640*480",
                        help="每帧分辨率，输入为字符串，格式为：帧宽*帧高，默认为640*480")
    args = parser.parse_args()

    return args


def resolution_reader(res_text) -> tuple[int, int] | ValueError:
    if "*" in res_text:
        return tuple(eval(params) for params in "640*480".split("*"))[0:2]
    else:
        return ValueError("输入分辨率有误！")


if __name__ == "__main__":
    args = parse_args("基于普通线性插值缩放指定视频文件或指定目录下所有视频文件至指定的分辨率、帧率。")
    # 单文件模式
    if args.single:
        input_path = input("请输入您的单个待处理视频：").replace('\\', '/').replace("\"", "")
        output_path = input("请输入您的输出目录：").replace('\\', '/').replace("\"", "")
        if args.create_folder is not None:
            output_path = f"{output_path}/{args.create_folder}"
            os.mkdir(output_path)
        name = os.path.split(input_path)[-1]
        single(input_path=input_path,
               output_path=output_path,
               fps=args.frame_per_sec,
               resolution=resolution_reader(args.resolution))
    # 批处理模式
    else:
        input_path = input("请输入您的待处理视频所在目录：").replace('\\', '/').replace("\"", "")
        output_path = input("请输入您的输出目录：").replace('\\', '/').replace("\"", "")
        if args.create_folder is not None:
            output_path = f"{output_path}/{args.create_folder}"
            os.mkdir(output_path)
        res = resolution_reader(args.resolution)
        batch(input_directory=input_path,
              output_directory=output_path,
              fps=args.frame_per_sec,
              resolution=res)

    input("处理完毕，任意键退出...")
