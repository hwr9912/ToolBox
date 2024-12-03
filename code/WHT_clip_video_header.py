import os
import cv2
import csv
import argparse
from tqdm import tqdm


def clip(input_video_path: str,
         output_video_path: str,
         header_time: int = 0):
    # 读取输入视频
    capture = cv2.VideoCapture(filename=input_video_path)
    # 读取视频属性
    width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = capture.get(cv2.CAP_PROP_FPS)
    fourcc = int(capture.get(cv2.CAP_PROP_FOURCC))
    # 加载输出api
    writer = cv2.VideoWriter(filename=output_video_path,
                             fourcc=fourcc, fps=fps,
                             frameSize=(width, height))
    # 标记变量
    frames_to_skip = header_time * fps
    # 跳过开头的帧
    capture.set(cv2.CAP_PROP_POS_FRAMES, frames_to_skip)
    # cv2.namedWindow("out")
    if capture.isOpened():
        # 读取视频并写入输出视频
        while True:
            ret, frame = capture.read()
            if not ret:
                break
            # cv2.imshow("out", frame)
            writer.write(frame)
    else:
        print("Error: 请检查视频能否播放.")
    # cv2.destroyAllWindows()
    capture.release()
    writer.release()


def batch(input_videos_dir: str,
          output_videos_dir: str,
          args):
    if args.all is not None:
        for f in tqdm(os.listdir(input_videos_dir)):
            try:
                clip(input_video_path=f"{input_videos_dir}/{f}",
                     output_video_path=f"{output_videos_dir}/{f}",
                     header_time=args.all)
            except:
                ValueError("请检查--all参数输入！")
    elif args.each is not None:
        csv_path = args.each.replace('\\', '/').replace("\"", "")
        with open(csv_path, mode='r', newline='', encoding='gbk') as file:
            reader = csv.reader(file)
            for row in reader:
                clip(input_video_path=f"{input_videos_dir}/{row[0]}",
                     output_video_path=f"{output_videos_dir}/{row[0]}",
                     header_time=eval(row[1]))
    return 0


def parse_args(text):
    print("██╗    ██╗██╗  ██╗████████╗ ██████╗  ██████╗ ██╗     \n"
          "██║    ██║██║  ██║╚══██╔══╝██╔═══██╗██╔═══██╗██║     \n"
          "██║ █╗ ██║███████║   ██║   ██║   ██║██║   ██║██║     \n"
          "██║███╗██║██╔══██║   ██║   ██║   ██║██║   ██║██║     \n"
          "╚███╔███╔╝██║  ██║   ██║   ╚██████╔╝╚██████╔╝███████╗\n"
          " ╚══╝╚══╝ ╚═╝  ╚═╝   ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝\n")
    print(f"本程序用于{text}")
    parser = argparse.ArgumentParser(description="对目录下所有视频根据指定时间长度裁剪视频开头，检测到多个输入优先执行单文件模式，其次为each模式")
    parser.add_argument("--each", "-e", type=str, default=None,
                        help="基于时间表格，表格为csv格式，无表头，第一列为文件名（不包含路径，但包含后缀），第二列为需要裁剪的时间长度(正整数，单位为s)，"
                             "参数后给出表格文件绝对地址，地址中不包含中文")
    parser.add_argument("--all", "-a", nargs="?", const=5, type=int, default=None,
                        help="基于相同时间长度（单位为秒）裁剪，命令行传参未给出输入值时则默认为5")
    parser.add_argument("--single", "-s", type=int, default=None,
                        help="处理单个视频")
    args = parser.parse_args()

    if args.each is None and args.all is None:
        args.all = eval(input("未检测到时长输入，请输入打算剪裁的时间长度："))

    return args



if __name__ == "__main__":
    args = parse_args("自动批量剪裁视频")

    if args.single is None:
        input_videos_dir = input("待处理视频所在目录：").replace('\\', '/').replace("\"", "")
        output_videos_dir = input("处理后视频保存目录：").replace('\\', '/').replace("\"", "")
        batch(input_videos_dir=input_videos_dir,
              output_videos_dir=output_videos_dir,
              args=args)
    else:
        input_video_path = input("待处理视频位置：").replace('\\', '/').replace("\"", "")
        output_video_path = input("处理后视频存放位置：").replace('\\', '/').replace("\"", "")
        try:
            clip(input_video_path=input_video_path,
                 output_video_path=output_video_path,
                 header_time=args.single)
        except:
            print("请检查--single参数输入！")

    input("处理完毕，按回车键退出...")

