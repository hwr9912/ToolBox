# pyinstaller -F .\code\WHT_shuffle_file_to_dataset.py
import os
import argparse
import random
from collections import defaultdict


def train_test_split(data, labels, train_size=0.2, random_state=None, stratify:list=None):
    """
    自定义数据集划分函数，支持分层抽样
    :param data: 数据集，可以是列表、numpy 数组等可迭代对象
    :param labels: 数据集对应的标签，长度应与 data 一致
    :param train_size: 测试集所占的比例，默认为 0.2
    :param random_state: 随机种子，用于保证结果的可重复性，默认为 None
    :param stratify: 分层抽样的依据，通常为标签列表。如果为 None，则不进行分层抽样
    :return: train_data, test_data, train_labels, test_labels: 划分后的训练数据、测试数据、训练标签和测试标签
    """
    if random_state is not None:
        random.seed(random_state)

    if len(data) != len(labels):
        raise ValueError("数据集和标签的长度不一致")

    if stratify is None:
        # 不进行分层抽样
        indices = list(range(len(data)))
        random.shuffle(indices)
        split_index = int(len(data) * train_size)
        train_indices = indices[:split_index]
        test_indices = indices[split_index:]
    else:
        # 进行分层抽样
        if len(labels) != len(stratify):
            raise ValueError("标签和分层依据的长度不一致")

        # 按分层依据对数据进行分组
        strata = defaultdict(list)
        for idx, label in enumerate(stratify):
            strata[label].append(idx)

        train_indices = []
        test_indices = []
        for label, indices in strata.items():
            random.shuffle(indices)
            split_index = int(len(indices) * train_size)
            train_indices.extend(indices[:split_index])
            test_indices.extend(indices[split_index:])

    # 根据索引提取数据和标签
    train_data = [data[i] for i in train_indices]
    test_data = [data[i] for i in test_indices]
    train_labels = [labels[i] for i in train_indices]
    test_labels = [labels[i] for i in test_indices]

    return train_data, test_data, train_labels, test_labels

def stratified_sample(root_dir, is_folder=True, train_ratio=0.8, test_ratio=0.2, val_ratio=0.2, random_state=1):
    """
    分层抽样生成数据集
    :param root_dir:样本文件夹地址，本目录下必须为文件夹，文件夹名为样本名
    :param is_folder:样本文件夹中包含的样本形式是否为文件夹，默认为是文件夹，反之为文件
    :param train_ratio:训练集比例
    :param test_ratio:测试集比例
    :param val_ratio:验证集比例
    :param random_state:随机数种子，默认为1
    :return:X_train, X_test, X_val 相对于root_dir的相对路径字符串列表
    """
    # 遍历根目录中的类别文件夹，提取所有类别名字符串
    categories = [category for category in os.listdir(root_dir) if os.path.isdir(os.path.join(root_dir, category))]
    all_samples = []
    all_labels = []

    # 逐类别文件夹提取样本名
    if is_folder:
        for category in categories:
            category_path = f"{root_dir}/{category}" # 类别文件夹地址
            samples = [os.path.join(category, sample) for sample in os.listdir(category_path)
                       if os.path.isdir(f"{category_path}/{sample}")] # 样本文件夹地址
            all_samples.extend(samples) # 添加到样本名列表
            all_labels.extend([category] * len(samples)) # 添加类别文件夹
    else:
        for category in categories:
            category_path = f"{root_dir}/{category}" # 类别文件夹地址
            samples = [os.path.join(category, sample) for sample in os.listdir(category_path)
                       if os.path.isfile(f"{category_path}/{sample}")] # 样本文件夹地址
            all_samples.extend(samples) # 添加到样本名列表
            all_labels.extend([category] * len(samples)) # 添加类别文件夹

    # 划分数据集
    # 第一次划分：训练集 vs 测试+验证集
    X_train, X_temp, y_train, y_temp = train_test_split(all_samples, all_labels, train_size=train_ratio/(train_ratio+test_ratio+val_ratio),
                                                        stratify=all_labels, random_state=random_state)

    # 第二次划分：测试集 vs 验证集
    X_test, X_val, y_test, y_val = train_test_split(X_temp, y_temp, train_size=val_ratio / (test_ratio + val_ratio),
                                                    stratify=y_temp, random_state=random_state)

    return X_train, X_test, X_val

def simple_sample(root_dir, is_folder=True, train_ratio=0.8, test_ratio=0.2, val_ratio=0.2, random_state=1):
    """
        分层抽样生成数据集
        :param root_dir:样本文件夹地址，本目录下必须为文件夹，文件夹名为样本名
        :param is_folder:样本文件夹中包含的样本形式是否为文件夹，默认为是文件夹，反之为文件
        :param train_ratio:训练集比例
        :param test_ratio:测试集比例
        :param val_ratio:验证集比例
        :param random_state:随机数种子，默认为1
        :return:X_train, X_test, X_val 相对于root_dir的相对路径字符串列表
        """
    # 逐类别文件夹提取样本名
    if is_folder:
        all_samples = [sample for sample in os.listdir(root_dir)
                       if os.path.isdir(f"{root_dir}/{sample}")] # 添加到样本名列表
    else:
        all_samples = [sample for sample in os.listdir(root_dir)
                       if os.path.isfile(f"{root_dir}/{sample}")]  # 添加到样本名列表
    all_labels = [0] * len(all_samples)

    # 划分数据集
    # 第一次划分：训练集 vs 测试+验证集
    X_train, X_temp, y_train, y_temp = train_test_split(
        all_samples, all_labels,
        train_size=train_ratio / (train_ratio + test_ratio + val_ratio),
        random_state=random_state)

    # 第二次划分：测试集 vs 验证集
    X_test, X_val, y_test, y_val = train_test_split(
        X_temp, y_temp,
        train_size=val_ratio / (test_ratio + val_ratio),
        random_state=random_state)

    return X_train, X_test, X_val

def options(text):
    print("██╗    ██╗██╗  ██╗████████╗ ██████╗  ██████╗ ██╗     \n"
          "██║    ██║██║  ██║╚══██╔══╝██╔═══██╗██╔═══██╗██║     \n"
          "██║ █╗ ██║███████║   ██║   ██║   ██║██║   ██║██║     \n"
          "██║███╗██║██╔══██║   ██║   ██║   ██║██║   ██║██║     \n"
          "╚███╔███╔╝██║  ██║   ██║   ╚██████╔╝╚██████╔╝███████╗\n"
          " ╚══╝╚══╝ ╚═╝  ╚═╝   ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝\n")
    print(f"欢迎使用WeHasTool. 我们将尝试{text}")
    parser = argparse.ArgumentParser(
        description="对给定目录随机抽样生成训练集、测试集和验证集，结果单独输出为列表")
    parser.add_argument("--encoding", "-e", type=str, default="utf-8",
                        help="编码格式，默认为utf-8")
    parser.add_argument("--folder_sample", "-f", action="store_true", default=False,
                        help="样本是否是文件夹格式，默认为文件格式")
    parser.add_argument("--random_seed", "-r", type=float, default=1,
                        help="随机数种子，默认为1")
    parser.add_argument("--stratified", "-s", action="store_true", default=False,
                        help="是否选择分层随机抽样，默认为简单随机抽样")
    parser.add_argument("--partially_selected_sample", "-p", type=float, default=None,
                        help=r"部分选取样本百分比，接受0-1之间的值，默认为1，超出范围的均默认为1")

    opt = parser.parse_args()
    if opt.partially_selected_sample is not None:
        if opt.partially_selected_sample > 1 or opt.partially_selected_sample < 0:
            opt.partially_selected_sample = 1

    return opt

if __name__ == "__main__":
    opt = options("对给定目录下所有样本文件或文件夹进行随机抽样，生成训练集、测试集和验证集，结果单独输出为列表。默认为非分层抽样模式。")

    input_path = input("请输入样本父目录：").replace('\\', '/').replace("\"", "")
    output_path = input("请输入结果文件输出目录：").replace('\\', '/').replace("\"", "")
    train_ratio = input("训练集比例或个数或比值(回车默认为0.8)：") or 0.8
    test_ratio = input("测试集比例或个数或比值(回车默认为0.2)：") or 0.2
    val_ratio = input("验证集比例或个数或比值(回车默认为0.2)：") or 0.2
    if opt.stratified:
        train, test, val = stratified_sample(root_dir=input_path, is_folder=opt.folder_sample,
                                             train_ratio=train_ratio, test_ratio=test_ratio, val_ratio=val_ratio,
                                             random_state=opt.random_seed)
    else:
        train, test, val = simple_sample(root_dir=input_path, is_folder=opt.folder_sample,
                                         train_ratio=train_ratio, test_ratio=test_ratio, val_ratio=val_ratio,
                                         random_state=opt.random_seed)

    if opt.partially_selected_sample is not None:
        for dataset in ['train', 'test', 'val']:
            sel = int(len(eval(dataset)) * opt.partially_selected_sample)
            with open(f"{output_path}/{dataset}.txt", "w", encoding=opt.encoding) as f:
                f.write("\n".join(eval(dataset)[:sel]))
    else:
        for dataset in ['train', 'test', 'val']:
            with open(f"{output_path}/{dataset}.txt", "w", encoding=opt.encoding) as f:
                f.write("\n".join(eval(dataset)))

    input("处理完毕，任意键退出...")