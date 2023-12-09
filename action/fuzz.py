import logging


class Fuzz:
    def __init__(self, input_data):
        self.input_data = input_data

    def run(self):
        # 实现 fuzz 操作的逻辑
        logging.info(f"Running fuzz with input_data: {self.input_data}")
