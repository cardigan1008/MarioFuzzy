import logging
import os
import random

from tqdm import tqdm

from action import run
from util.mutator_schedule.mutator_schedule import MutatorSchedule
from util.preprocess import constants as c
from util.seed_schedule.seed_schedule import SeedSchedule


def read_file_content(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            return content
    except Exception as e:
        logging.error(f"Error while reading file {file_path}: {e}")
        return None


def sort_tuples(tuples_list):
    sorted_tuples = sorted(tuples_list, key=lambda x: x[1], reverse=True)
    return sorted_tuples


def select_tuples(sorted_tuples, high_ratio):
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
        for i in tqdm(range(len(file_list)), "Loading seeds"):
            tmp_ops = read_file_content(file_list[i])
            _, gold, score = run.play_game(tmp_ops, len(tmp_ops))
            seed_score_pairs.append((tmp_ops, score))

        while True:
            seed_schedule = SeedSchedule(seed_score_pairs)
            selected_tuple = seed_schedule.schedule()

            energy = min(len(selected_tuple[0]), c.OP_COUNT_BASELINE * (selected_tuple[1] / c.SCORE_BASELINE))

            mutation_schedule = MutatorSchedule(selected_tuple, energy)
            output_data, score, is_crash = mutation_schedule.schedule()

            if is_crash:
                self.save_crash_data(output_data)
                continue
            else:
                seed_score_pairs.append((output_data, score))
                self.save_output_data(output_data)

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

    def save_crash_data(self, data):
        # 获取当前输出文件的序号，如 seed1.txt、seed2.txt 等
        crash_file_number = len([f for f in os.listdir(self.crash_path) if f.startswith("crash")]) + 1
        crash_file_name = f"seed{crash_file_number}.txt"

        # 构建输出文件路径
        crash_file_path = os.path.join(self.crash_path, crash_file_name)

        # 保存数据到输出文件
        try:
            with open(crash_file_path, 'w') as crash_file:
                crash_file.write(data)
            logging.info(f"Crash data saved to {crash_file_path}")
        except Exception as e:
            logging.error(f"Error while saving crash data: {e}")

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
