import os
import cv2
import argparse

def extract_frames(video_path, output_folder, interval, start=0):
    """
    对单个文件提取截图
    :param video_path: 视频文件地址
    :param output_folder: 输出地址
    :param interval: 间隔帧数
    :return:
    """
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print(f"Error: Could not open video {video_path}.")
        return

    frame_count = 0
    saved_frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if interval == 0 or frame_count % interval == 0:
            frame_filename = os.path.join(output_folder, f"frame_{saved_frame_count + start:05d}.jpg")
            cv2.imwrite(frame_filename, frame)
            saved_frame_count += 1

        frame_count += 1

    cap.release()
    print(f"共计从{video_path}遍历了{frame_count}帧并保存了{saved_frame_count}帧于{output_folder}")
    return saved_frame_count


def process_all_videos_in_directory(input_directory, output_directory, args):
    if not os.path.exists(input_directory):
        ValueError("请检查输入路径！")
    if not os.path.exists(output_directory):
        ValueError("请检查输出路径！")

    if args.multiple_folder:
        # 输出
        for filename in os.listdir(input_directory):
            if filename.endswith(".mp4") or filename.endswith(".avi") or filename.endswith(".mov"):
                # 在输出目录下单独创建文件夹
                video_output_folder = os.path.join(output_directory, os.path.splitext(filename)[0])
                os.makedirs(video_output_folder)
                extract_frames(video_path=os.path.join(input_directory, filename),
                               output_folder=video_output_folder,
                               interval=args.interval)
    elif args.one_folder is not None:
        # 在输出目录下创建文件夹
        video_output_folder = os.path.join(output_directory, args.one_folder)
        os.makedirs(video_output_folder)
        # 帧计数
        all_frame_count = 0
        # 输出
        for filename in os.listdir(input_directory):
            if filename.endswith(".mp4") or filename.endswith(".avi") or filename.endswith(".mov"):
                frame_count = extract_frames(video_path=os.path.join(input_directory, filename),
                                             output_folder=video_output_folder,
                                             interval=args.interval,
                                             start=all_frame_count)
                all_frame_count += frame_count
    else:
        # 输出目录
        video_output_folder = output_directory
        # 帧计数
        all_frame_count = 0
        # 输出
        for filename in os.listdir(input_directory):
            if filename.endswith(".mp4") or filename.endswith(".avi") or filename.endswith(".mov"):
                frame_count = extract_frames(video_path=os.path.join(input_directory, filename),
                                             output_folder=video_output_folder,
                                             interval=args.interval,
                                             start=all_frame_count)
                all_frame_count += frame_count


def parse_args(text):
    print("██╗    ██╗██╗  ██╗████████╗ ██████╗  ██████╗ ██╗     \n"
          "██║    ██║██║  ██║╚══██╔══╝██╔═══██╗██╔═══██╗██║     \n"
          "██║ █╗ ██║███████║   ██║   ██║   ██║██║   ██║██║     \n"
          "██║███╗██║██╔══██║   ██║   ██║   ██║██║   ██║██║     \n"
          "╚███╔███╔╝██║  ██║   ██║   ╚██████╔╝╚██████╔╝███████╗\n"
          " ╚══╝╚══╝ ╚═╝  ╚═╝   ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝\n")
    print(f"本程序用于{text}")
    parser = argparse.ArgumentParser(description="从视频中提取每一帧作为图像并输出")
    parser.add_argument("--single", "-s", action="store_true", default=False,
                        help="处理单个文件，默认为批处理模式")
    parser.add_argument("--interval", "-i", type=int, default=30,
                        help="保存帧的时间间隔，默认为 30（每帧保存一次）")
    parser.add_argument("--number", "-n", type=int, default=0,
                        help="起始编号，默认从0开始(仅适用于单文件模式,目录模式下所有视频均单独保存于文件夹中)")
    parser.add_argument("--multiple_folder", "-m", action="store_true", default=False,
                        help="每个视频对应创建一个存储截屏的文件夹")
    parser.add_argument("--one_folder", "-o", nargs='?', const="Frame2Jpg", type=str, default=None,
                        help="所有视频均对应同一个新建的存储截屏的文件夹，名字默认为Frame2Jpg，需要修改名字可给出字符串")

    args = parser.parse_args()

    return args


if __name__ == "__main__":
    args = parse_args("给出视频文件地址(不能包含中文)，并按指定的间隔帧数将视频转化为截图, 默认存储于给出目录下的一个新建同名文件夹。")

    if args.single:
        video_path = input("输入待处理视频的地址: ")
        output_folder = input("输入导出图片的输出目录: ")
        video_path = video_path.replace('\\', '/').replace("\"", "")
        output_folder = output_folder.replace('\\', '/').replace("\"", "")
        extract_frames(video_path=video_path,
                       output_folder=output_folder,
                       interval=args.interval,
                       start=args.number)
    else:
        input_directory = input("输入待处理视频的输入目录: ")
        output_directory = input("输入导出图片的输出目录: ")
        input_directory = input_directory.replace('\\', '/').replace("\"", "")
        output_directory = output_directory.replace('\\', '/').replace("\"", "")
        process_all_videos_in_directory(input_directory=input_directory,
                                        output_directory=output_directory,
                                        args=args)
