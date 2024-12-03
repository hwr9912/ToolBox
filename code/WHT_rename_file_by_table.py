import os
import csv


# 输入文件所属目录
def rename(input_directory: str):
    if input_directory.endswith(".csv"):
        # 打开 CSV 文件
        with open(input_directory, mode='r', newline='', encoding='gbk') as file:
            reader = csv.reader(file)
            # 遍历每一行
            error_count = 0
            for total, row in enumerate(reader):
                origin = row[0].replace('\\', '/').replace("\"", "")
                new = "{}/{}".format(os.path.split(origin)[0], row[1])
                try:
                    os.renames(origin, new)
                except:
                    error_count += 1
                    print(f"{origin}无法重命名！")
    else:
        print("无法读取表格!")
        return -1
    print(f"共计{total+1}个重命名要求中，出现了{error_count}个错误，其余均重命名完毕！")
    return 0


if __name__ == "__main__":
    print("给出对应csv表（第一列是绝对路径，可用ctrl+shift+c复制到excel中）后，按表重命名所有文件")
    input_directory = input("输入对应表所在路径: ")
    input_directory = input_directory.replace('\\', '/').replace("\"", "")
    rename(input_directory=input_directory)
    input("回车键退出...")
