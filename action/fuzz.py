import logging
import os
import random

from action import transform
from action import run
from util import SA1


def read_file_content(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            return content
    except Exception as e:
        logging.error(f"Error while reading file {file_path}: {e}")
        return None


import random


def sort_tuples(tuples_list):
    sorted_tuples = sorted(tuples_list, key=lambda x: x[1], reverse=True)
    return sorted_tuples


def select_tuples(sorted_tuples, high_ratio, random_ratio):
    total_tuples = len(sorted_tuples)
    high_count = int(total_tuples * high_ratio)

    high_tuples = sorted_tuples[:high_count]
    random_tuple = random.choice(sorted_tuples[high_count:])

    selected_tuple = random.choice(high_tuples + [random_tuple])
    return selected_tuple


class Fuzz:
    def __init__(self, target_path, crash_path):
        self.target_path = target_path
        self.crash_path = crash_path

    def run(self):
        file_list = self.get_file_list()
        seed_score_pairs = []
        for i in range(len(file_list)):
            tmp_ops = read_file_content(file_list[i])
            _, gold, score = run.play_game(tmp_ops)
            seed_score_pairs.append((tmp_ops, score))

        #     seed = file_list.__getitem__(i)
        #     seed_score_pairs.append((seed, SA1.get_score(seed)))
        round = 0
        while True:
            sorted_tuples = sort_tuples(seed_score_pairs)
            high_ratio = 0.7
            random_ratio = 0.3

            selected_tuple = select_tuples(sorted_tuples, high_ratio, random_ratio)
            seed_score_pairs.remove(selected_tuple)
            # logging.info(f"Begin to fuzz with seed: {cur_seed}")
            # operation_list = read_file_content(self.target_path + cur_seed)

            # transform_action = transform.Transform(operation_list)
            # output_data = transform_action.transform()
            # 保存 output_data 到新文件

            # self.save_output_data(output_data)

            # 运行游戏
            # run.play_game(output_data)
            output_data, score = SA1.simulated_annealing_optimization(selected_tuple)
            self.save_output_data(output_data)
        return output_data, score

    def single_run(self, seed):
        # 加载seed
        logging.info(f"Begin to fuzz with seed: {seed}")
        operation_list = read_file_content(self.target_path + seed)
        # 运行
        score = 0  # TODO: get real score
        return seed, score

    def seed_select(self):
        return " "

    def save_output_data(self, data):
        # 获取当前输出文件的序号，如 seed1.txt、seed2.txt 等
        output_file_number = len([f for f in os.listdir(self.target_path) if f.startswith("seed")]) + 1
        output_file_name = f"seed{output_file_number}.txt"

        # 构建输出文件路径
        output_file_path = os.path.join(self.target_path, output_file_name)

        # 保存数据到输出文件
        try:
            with open(output_file_path, 'w') as output_file:
                output_file.write(data)
            logging.info(f"Output data saved to {output_file_path}")
        except Exception as e:
            logging.error(f"Error while saving output data: {e}")

    def get_file_list(self):
        # 使用 os 模块的 listdir 函数获取目标路径下的所有文件和文件夹
        try:
            files = os.listdir(self.target_path)
            # 过滤掉目录，只保留文件
            file_list = [f for f in files if os.path.isfile(os.path.join(self.target_path, f))]
            return file_list
        except Exception as e:
            logging.error(f"Error while getting file list: {e}")
            return []
