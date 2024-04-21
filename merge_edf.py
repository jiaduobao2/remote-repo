import os
import numpy as np
from pyedflib import highlevel
import warnings
from tqdm import tqdm
def merge_edf_files(directory_path, output_file_path, batch_size=10,headername='cdkl1'):
    # 获取目录中的所有EDF文件路径
    file_paths = [os.path.join(directory_path, file) for file in os.listdir(directory_path) if file.endswith('.edf')]
    file_paths.sort()
    # file_paths = sorted(file_paths)


    # # 初始化用于存储合并后信号的列表和标注信息列表
    merged_signals = []
    all_max = []
    all_min = []
    merged_annotations = []
    duration = 0
    file_count = 0
    output_file_count = 0
    # # 遍历每个EDF文件
    for file_path in tqdm(file_paths):
        # print(file_path)
        try:
            signals, _, _ = highlevel.read_edf(file_path)
        except Exception as e:
            print(f"Error reading file: {file_path}. Skipping this file.")
            continue

        # 将信号和统计信息添加到列表中
        merged_signals.append(signals)
        all_max.append(np.max(signals))
        all_min.append(np.min(signals))

        # 获取当前EDF文件的注释信息并调整时间
        annotations = highlevel.read_edf(file_path)[2]['annotations']
        for annotation in annotations:
            annotation[0] += duration
            merged_annotations.append(annotation)

        # 获取EDF文件的长度
        duration += signals.shape[1] / 256  # 假设采样率为 256 Hz

        file_count += 1

        # 当达到指定的 batch_size 时进行合并并写入文件
        if file_count >= batch_size:
            # 合并信号列表
            merged_signals = np.concatenate(merged_signals, axis=1)

            # 确定动态的 physical_max 和 physical_min
            dynamic_physical_max = max(all_max)
            dynamic_physical_min = min(all_min)

            # 创建合并后的 signal_headers
            signal_headers = highlevel.make_signal_headers(['ch1', 'ch2', 'ch3', 'ch4'], sample_frequency=256,
                                                           physical_max=dynamic_physical_max, physical_min=dynamic_physical_min)

            # 获取第一个EDF文件的header，用于写入合并后的EDF文件
            _, _, header = highlevel.read_edf(file_paths[0])

            # 更新合并后的header的注释信息
            header['annotations'] = merged_annotations

            # 构建输出文件路径
            output_file_name = f"{headername}_{output_file_count}.edf"
            output_file_path_full = os.path.join(output_file_path, output_file_name)

            # 创建合并后的EDF文件
            highlevel.write_edf(output_file_path_full, merged_signals, signal_headers=signal_headers, header=header)

            # 重置合并数据和计数器
            merged_signals = []
            all_max = []
            all_min = []
            merged_annotations = []
            duration = 0
            file_count = 0
            output_file_count += 1

    # 处理剩余的文件（如果有）
    if file_count > 0:
        # 合并信号列表
        merged_signals = np.concatenate(merged_signals, axis=1)

        # 确定动态的 physical_max 和 physical_min
        dynamic_physical_max = max(all_max)
        dynamic_physical_min = min(all_min)

        # 创建合并后的 signal_headers
        signal_headers = highlevel.make_signal_headers(['ch1', 'ch2', 'ch3', 'ch4'], sample_frequency=256,
                                                       physical_max=dynamic_physical_max, physical_min=dynamic_physical_min)

        # 获取第一个EDF文件的header，用于写入合并后的EDF文件
        _, _, header = highlevel.read_edf(file_paths[0])

        # 更新合并后的header的注释信息
        header['annotations'] = merged_annotations

        # 构建输出文件路径
        output_file_name = f"{headername}_{output_file_count}.edf"
        output_file_path_full = os.path.join(output_file_path, output_file_name)

        # 创建合并后的EDF文件
        highlevel.write_edf(output_file_path_full, merged_signals, signal_headers=signal_headers, header=header)
# 示例用法
def merge_edf_files2(directory_path, output_file_path, batch_size=10,headername='cdkl1'):
    # 获取目录中的所有EDF文件路径
    file_paths = [os.path.join(directory_path, file) for file in os.listdir(directory_path) if file.endswith('.edf')]
    file_paths.sort()
    # file_paths = sorted(file_paths)
    # # 初始化用于存储合并后信号的列表和标注信息列表
    merged_signals = []
    all_max = []
    all_min = []
    merged_annotations = []
    duration = 0
    file_count = 0
    output_file_count = 0
    # # 遍历每个EDF文件
    for file_path in tqdm(file_paths):
        # print(file_path)
        try:
            signals, _, _ = highlevel.read_edf(file_path)
        except Exception as e:
            print(f"Error reading file: {file_path}. Skipping this file.")
            continue

        # 将信号和统计信息添加到列表中
        merged_signals.append(signals)
        all_max.append(np.max(signals))
        all_min.append(np.min(signals))
        file_count += 1

        # 当达到指定的 batch_size 时进行合并并写入文件
        if file_count >= batch_size:
            # 合并信号列表
            merged_signals = np.concatenate(merged_signals, axis=1)

            # 确定动态的 physical_max 和 physical_min
            dynamic_physical_max = max(all_max)
            dynamic_physical_min = min(all_min)

            # 创建合并后的 signal_headers
            signal_headers = highlevel.make_signal_headers(['ch1', 'ch2', 'ch3', 'ch4'], sample_frequency=256,
                                                           physical_max=dynamic_physical_max, physical_min=dynamic_physical_min)

            # 获取第一个EDF文件的header，用于写入合并后的EDF文件
            _, _, header = highlevel.read_edf(file_paths[0])

            # 更新合并后的header的注释信息
            # header['annotations'] = merged_annotations

            # 构建输出文件路径
            output_file_name = f"{headername}_{output_file_count}_.edf"
            output_file_path_full = os.path.join(output_file_path, output_file_name)

            # 创建合并后的EDF文件
            highlevel.write_edf(output_file_path_full, merged_signals, signal_headers=signal_headers, header=header)

            # 重置合并数据和计数器
            merged_signals = []
            all_max = []
            all_min = []
            merged_annotations = []
            duration = 0
            file_count = 0
            output_file_count += 1

    # 处理剩余的文件（如果有）
    if file_count > 0:
        # 合并信号列表
        merged_signals = np.concatenate(merged_signals, axis=1)

        # 确定动态的 physical_max 和 physical_min
        dynamic_physical_max = max(all_max)
        dynamic_physical_min = min(all_min)

        # 创建合并后的 signal_headers
        signal_headers = highlevel.make_signal_headers(['ch1', 'ch2', 'ch3', 'ch4'], sample_frequency=256,
                                                       physical_max=dynamic_physical_max, physical_min=dynamic_physical_min)

        # 获取第一个EDF文件的header，用于写入合并后的EDF文件
        _, _, header = highlevel.read_edf(file_paths[0])
        # 构建输出文件路径
        output_file_name = f"{headername}_{output_file_count}.edf"
        output_file_path_full = os.path.join(output_file_path, output_file_name)

        # 创建合并后的EDF文件
        highlevel.write_edf(output_file_path_full, merged_signals, signal_headers=signal_headers, header=header)
def merge_edf_files3(directory_path, output_file_path, batch_size=10, headername='cdkl1'):
    # 获取目录中的所有EDF文件路径
    file_paths = [os.path.join(directory_path, file) for file in os.listdir(directory_path) if file.endswith('.edf')]
    file_paths.sort()

    merged_signals = []
    all_max = []
    all_min = []
    file_count = 0
    output_file_count = 0
    batch_first_filename = None  # 用于存储每批次的第一个文件名

    for file_path in tqdm(file_paths):
        try:
            signals, _, _ = highlevel.read_edf(file_path)
        except Exception as e:
            print(f"Error reading file: {file_path}. Skipping this file.")
            continue

        merged_signals.append(signals)
        all_max.append(np.max(signals))
        all_min.append(np.min(signals))
        file_count += 1

        if file_count == 1:  # 记录每个批次的第一个文件名
            batch_first_filename = os.path.splitext(os.path.basename(file_path))[0]

        if file_count >= batch_size:
            merged_signals = np.concatenate(merged_signals, axis=1)

            dynamic_physical_max = max(all_max)
            dynamic_physical_min = min(all_min)

            signal_headers = highlevel.make_signal_headers(['ch1', 'ch2', 'ch3', 'ch4'], sample_frequency=256,
                                                           physical_max=dynamic_physical_max, physical_min=dynamic_physical_min)

            # 构建输出文件路径，包含批次第一个文件名
            output_file_name = f"{headername}_{output_file_count}_{batch_first_filename}_{os.path.splitext(os.path.basename(file_path))[0]}.edf"
            output_file_path_full = os.path.join(output_file_path, output_file_name)

            _, _, header = highlevel.read_edf(file_paths[0])

            highlevel.write_edf(output_file_path_full, merged_signals, signal_headers=signal_headers, header=header)

            merged_signals = []
            all_max = []
            all_min = []
            merged_annotations = []
            duration = 0
            file_count = 0
            output_file_count += 1

    if file_count > 0:
        merged_signals = np.concatenate(merged_signals, axis=1)

        dynamic_physical_max = max(all_max)
        dynamic_physical_min = min(all_min)

        signal_headers = highlevel.make_signal_headers(['ch1', 'ch2', 'ch3', 'ch4'], sample_frequency=256,
                                                       physical_max=dynamic_physical_max, physical_min=dynamic_physical_min)

        output_file_name = f"{headername}_{output_file_count}_{batch_first_filename}.edf"  # 最后一个文件的标识
        output_file_path_full = os.path.join(output_file_path, output_file_name)

        _, _, header = highlevel.read_edf(file_paths[0])

        highlevel.write_edf(output_file_path_full, merged_signals, signal_headers=signal_headers, header=header)
if __name__ == "__main__":
    '''该程序的作用是把分散的的edf文件合并成一个整体，处理完成后传给process_edfdata_to_npysegement.py进一步处理'''
    warnings.filterwarnings('ignore')
    # 指定包含要合并的EDF文件的目录
    directory_path = '/mnt/sda/年后小鼠/edf_directory/cdkl4_edf/'
    headername = directory_path.split('/')[-2].split('_')[0]
    print(headername)

    # 指定合并后的EDF文件路径,注意修改合并后的文件名
    output_file_path = r'/mnt/sda/年后小鼠/merged/'

    # 合并EDF文件
    merge_edf_files3(directory_path, output_file_path,batch_size=24,headername=headername)
