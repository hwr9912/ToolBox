import os
import cv2
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="从原始彩色图像中提取灰度图像并输出")
    parser.add_argument("--threshold", "-t", action="store_true", help="进行二值化")
    parser.add_argument("--maxvalue", "-m", type=int, default=255,
                        help="二值化中的最大值")

    args = parser.parse_args()

    fig_dir = input("输入原始图像路径：").replace("\\", "/").replace("\"", "")
    save_dir = input("输入灰度图像保存路径：").replace("\\", "/").replace("\"", "")
    for file in os.listdir(fig_dir):
        src = cv2.imread(f"{fig_dir}/{file}")
        # 图像处理
        dst = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
        if args.threshold:
            _, dst = cv2.threshold(dst, 0, args.maxvalue, cv2.THRESH_BINARY)
        # 图像保存
        cv2.imwrite(f"{save_dir}/{file}", dst)
