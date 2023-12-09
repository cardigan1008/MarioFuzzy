import logging
import os
import random

from action import transform
from action import run

def read_file_content(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            return content
    except Exception as e:
        logging.error(f"Error while reading file {file_path}: {e}")
        return None


class Fuzz:
    def __init__(self, target_path, crash_path):
        self.target_path = target_path
        self.crash_path = crash_path

    def run(self):
        logging.info(f"Begin to fuzz with target_path: {self.target_path}, crash_path: {self.crash_path}")

        file_list = self.get_file_list()
        cur_seed = random.choice(file_list)  # TODO: implement selection
        operation_list = read_file_content(self.target_path + cur_seed)

        transform_action = transform.Transform(operation_list)
        output_data = transform_action.transform()

        logging.info(f"Transformed data: {output_data}")

        # 保存 output_data 到新文件
        self.save_output_data(output_data)

        # 运行游戏
        run.play_game(output_data)

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
