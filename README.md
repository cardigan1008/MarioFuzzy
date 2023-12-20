# MarioFuzzy
A fuzz tool for super mario game.



## 架构分析

### 程序入口

程序入口为main.py。1

```python
coloredlogs.install(level='INFO', fmt='%(asctime)s - %(levelname)s - %(message)s')


def main():
    logging.info("Welcome to mario fuzz!")
    parse_and_run()


if __name__ == '__main__':
    main()
```



### CLI

使用argparse对命令行选项、参数进行解析。

增加了operation参数，并分类为transform与fuzz命令，分别用于测试单次变异和完整模糊测试。并指定了input_data，即原始种子所在路径。

```python
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
    fuzz_parser.add_argument('seed_path', help='Path of seeds for the fuzz operation')
    fuzz_parser.set_defaults(func=fuzz_cmd)

    # 解析命令行参数并执行相应的操作
    args = parser.parse_args()
    args.func(args)
```





## Usage

### Fuzz
```
python main.py fuzz <input_data>
```

### Transform
```
python main.py transform <input_data>
```
Please make sure to modify the `game_path` in the `config.yaml` file located in the `action` folder to your own game's absolute path.