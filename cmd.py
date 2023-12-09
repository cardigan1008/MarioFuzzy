import argparse
import logging
from action import fuzz
from action import transform


def transform_cmd(args):
    # 处理 transform 操作，args 包含传递的参数
    logging.info(f"Begin to transform with input_data: {args.input_data}")
    fuzz_action = fuzz.Fuzz(args.input_data)
    fuzz_action.run()


def fuzz_cmd(args):
    # 处理 fuzz 操作，args 包含传递的参数
    logging.info(f"Begin to fuzz with input_data: {args.input_data}")


def parse_and_run():
    parser = argparse.ArgumentParser(description='A fuzz tool for super mario game.')
    subparsers = parser.add_subparsers(dest='operation', help='Operation to perform')

    # 添加 transform 子命令
    transform_parser = subparsers.add_parser('transform',
                                             help='Transform the program with specific rules')
    transform_parser.add_argument('input_data', help='Input data for the transform operation')
    transform_parser.set_defaults(func=transform_cmd)

    # 添加 fuzz 子命令
    fuzz_parser = subparsers.add_parser('fuzz', help='Fuzz the game')
    fuzz_parser.add_argument('input_data', help='Input data for the fuzz operation')
    fuzz_parser.set_defaults(func=fuzz_cmd)

    # 解析命令行参数并执行相应的操作
    args = parser.parse_args()
    args.func(args)
