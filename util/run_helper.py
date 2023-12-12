import logging
import os


def read_file_content(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            return content
    except Exception as e:
        logging.error(f"Error while reading file {file_path}: {e}")
        return None



class run_helper:
    def single_run(self, seed):
        # 加载seed
        logging.info(f"Begin to fuzz with seed: {seed}")
        operation_list = read_file_content(self.target_path + seed)
        # 运行
        score = 0  # TODO: get real score
        return seed, score
