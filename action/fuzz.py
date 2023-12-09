import logging
import os

from action import transform


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
        operation_list = read_file_content(file_list[0])  # TODO: implement selection
        # TODO: run with operation_list

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
