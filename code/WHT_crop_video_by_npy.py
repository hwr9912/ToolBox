import os
import cv2
import argparse
import numpy as np
from tqdm import tqdm


def video_by_mask(input_video_path: str = r"D:\Python\computer_vision\unet_water_maze\data\20240822WM1.avi",
                  input_mask_path: str = r"D:\Python\computer_vision\unet_water_maze\data\background.npy",
                  output_video_path: str = r"D:\Python\computer_vision\unet_water_maze\data",
                  suffix: str = "avi"):
    """
    输入视频文件和npy格式的 0-1 mask文件，输出裁剪过的视频
    :param input_video_path: 输入视频
    :param input_mask_path: 输入mask文件(0为裁剪部分)
    :param output_video_path: 输出视频
    :param suffix: 输出文件后缀
    :return: 无返回值
    """
    # 读取视频
    cap = cv2.VideoCapture(input_video_path)
    # 获取视频的宽度、高度和帧率
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    # 读取mask数据(load进来的是np.int32类型的数据，计算后结果也会变成int32类型的数据)
    mask = np.uint8(np.load(input_mask_path))
    # 定义编解码器并创建 VideoWriter 对象
    fourcc = cv2.VideoWriter.fourcc(*'XVID')  # 使用 'XVID' 编解码器
    if suffix == "mp4":
        fourcc = cv2.VideoWriter.fourcc(*'MP4V')
    # 设置输出文件名
    fname = os.path.split(input_video_path)[-1].split(".")[0]
    out = cv2.VideoWriter(f"{output_video_path}/crop_{fname}.{suffix}", fourcc, fps, (frame_width, frame_height))

    if cap.isOpened():
        # 循环读取视频帧
        while True:
            ret, frame = cap.read()

            # 如果读取成功，ret 为 True
            if not ret:
                break

            try:
                result = frame * mask
            except:
                mask_3d = np.repeat(mask[:, :, np.newaxis], 3, axis=2)
                result = frame * mask_3d

            out.write(result)
    else:
        print("Error: 请检查视频能否播放.")

    # 释放视频捕获对象
    cap.release()
    out.release()


def batch(input_video_dir, input_mask_path, output_video_dir, suffix: str = "avi"):
    """
    批处理封装函数
    :param input_video_dir:视频所在目录
    :param input_mask_path: mask文件地址
    :param output_video_dir: 输出视频文件夹所在目录
    :param suffix: 文件后缀
    :return:无返回值
    """
    if not os.path.exists(output_video_dir):
        os.mkdir(output_video_dir)
    count = 0
    for f in tqdm(os.listdir(input_video_dir)):
        if not f.endswith("avi") or f.endswith("mp4"):
            continue
        try:
            video_by_mask(input_video_path=f"{input_video_dir}/{f}",
                          input_mask_path=input_mask_path,
                          output_video_path=output_video_dir,
                          suffix=suffix)
            count += 1
        except:
            continue
    return count


if __name__ == "__main__":
    print("基于npy格式的mask文件剪裁视频文件。")
    parser = argparse.ArgumentParser(description="基于npy格式的mask文件剪裁视频文件，输出默认为无符号8位rgb的avi格式视频")
    parser.add_argument("--batch", "-b", action="store_true", help="剪裁目录下的所有视频文件")
    parser.add_argument("--not_create_folder", "-n", action="store_true", default=False,
                        help="不创建一个存储所有视频的文件夹（仅支持批处理模式，单文件模式无效果）")
    parser.add_argument("--suffix", "-s", type=str, default="avi", help="输出图像格式，默认为avi格式")

    args = parser.parse_args()

    # 批量处理
    if args.batch:
        input_video_folder = input("输入待处理视频所在目录: ")
        input_mask_file = input("输入mask文件（npy格式，确保尺寸相同）所在目录: ")
        output_video_folder = input("输入处理后视频输出文件夹所在目录: ")
        input_video_folder = input_video_folder.replace('\\', '/').replace("\"", "")
        input_mask_file = input_mask_file.replace('\\', '/').replace("\"", "")
        output_video_folder = output_video_folder.replace('\\', '/').replace("\"", "")
        # 函数内置了新建文件夹功能
        if not args.not_create_folder:
            output_video_folder = os.path.join(output_video_folder, "CropVideoByMask")
        count = batch(input_video_folder, input_mask_file, output_video_folder, suffix=args.suffix)
    # 单文件处理
    else:
        input_video_file = input("输入待处理视频文件目录: ")
        input_mask_file = input("输入mask文件（npy格式，确保尺寸相同）所在目录: ")
        output_video_folder = input("输入处理后视频输出目录: ")
        input_video_file = input_video_file.replace('\\', '/').replace("\"", "")
        input_mask_file = input_mask_file.replace('\\', '/').replace("\"", "")
        output_video_folder = output_video_folder.replace('\\', '/').replace("\"", "")
        video_by_mask(input_video_file, input_mask_file, output_video_folder, suffix=args.suffix)
        count = 1

    input(f"共处理了{count}个视频，任意键退出...")
