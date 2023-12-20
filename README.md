# MarioFuzzy
A fuzz tool for super mario game.

## Usage

### Transform

```shell
python main.py transform <input_data>
```

- `<input_data>`: Input data used for the transformation operation.

### Fuzz

```shell
python main.py fuzz <seed_path> <crash_path>
```

- `<seed_path>`: Path to the seed data for the fuzzing operation.
- `<crash_path>`: Path to the crash data for saving crash reports during the fuzzing process.

## Requirements

Game: [Mario-Level-1](https://github.com/justinmeister/Mario-Level-1)

Required Packages: Please refer to the `requirements.txt` file for the list of required packages.

## Notes

Please make sure to modify the `game_path` in the `config.yaml` file located in the `action` folder to your own game's absolute path.

------

## Overview

南京大学软件学院软件测试课程代码作业，选题方向为**程序分析-模糊测试**。

实现命令行工具形式的基于变异的模糊器，**设计思路**如下：

1. 定义测试输入：一组游戏操作的序列，五元组={left, right, up, jump, fire}
2. 定义输出：o={is_mario, gold, score}， is_mario=mario是否存在画面中；gold=金币数量；score=游戏得分
3. 种子调度，基于feedback
   1. 种子优先级排序：得分更高序列优先
   2. 能量分配：根据feedback结果，对照基准线分配energy
4. 测试生成：五种变异算子，并使用退火算法进行变异算子调度
5. 游戏执行，并截图保存
6. 结果分析：使用图像识别训练模型，识别分析状态返回结果
7. 结果保存：保存所有产生唯一状态的测试输入

**本项目特点**如下：

- **面向新的模糊目标**：测试目标为经典游戏[超级马里奥](https://github.com/justinmeister/Mario-Level-1)
- **添加新机制**
  - 更多样的变异算子：新增Shuffle变异算子
  - 变异算子调度：使用退火算法实现
  - 新颖的输出分析策略：训练图像识别模型，对游戏结果截图进行图像识别后获得游戏分数等信息

## Design

本项目架构如下：

- **action**: 包含与执行相关的文件
  - `config.yaml`: 配置文件
  - `fuzz.py`: Fuzz操作
  - `run.py`: 游戏运行
  - `transform.py`: Transform操作
- **test**: 测试相关的文件
- **util**: 工具类
  - `mutator_schedule`: 变异算子调度工具
  - `output_analysis`: 输出分析工具
  - `preprocess`: 预处理工具
  - `seed_schedule`: 种子调度工具

- `command.py`: 命令解析

- `main.py`: 执行入口

- `README.md`: 项目的说明文档

- `requirements.txt`: 项目所需的依赖包列表

### Main

> main.py

```python
coloredlogs.install(level='INFO', fmt='%(asctime)s - %(levelname)s - %(message)s')


def main():
    logging.info("Welcome to mario fuzz!")
    parse_and_run()


if __name__ == '__main__':
    main()
```

### CLI

> command.py

使用`argparse`对命令行选项、参数进行解析。

增加了`operation`参数，并分为`transform`与`fuzz`命令。

```python
def parse_and_run():
    parser = argparse.ArgumentParser(description='A fuzz tool for super mario game.')
    subparsers = parser.add_subparsers(dest='operation', help='Operation to perform')

    # 添加 transform 子命令
    transform_parser = subparsers.add_parser('transform',
                                             help='Transform the seed with one specific rules')
    transform_parser.add_argument('input_data', help='Input data for the transform operation')
    transform_parser.set_defaults(func=transform_cmd)

    # 添加 fuzz 子命令
    fuzz_parser = subparsers.add_parser('fuzz', help='Fuzz the game')
    fuzz_parser.add_argument('seed_path', help='Path of seeds for the fuzz operation')
    fuzz_parser.add_argument('crash_path', help='Path of crash data for the fuzz operation')
    fuzz_parser.set_defaults(func=fuzz_cmd)

    # 解析命令行参数并执行相应的操作
    args = parser.parse_args()
    args.func(args)
```

transform操作用于对指定的种子进行特定变异操作，尤其在前期开发对变异算子部分测试使用。

fuzz操作用于模糊测试，需要用户指定种子路径与crash存放路径。

### Action

本模块包括Fuzz, Transform, Run三种操作

#### Fuzz

> fuzz.py

初始化使用用户定义的`target_path`和`crash_path`来指定种子路径和崩溃路径。

```python
def __init__(self, target_path, crash_path):
    self.target_path = target_path
    self.crash_path = crash_path
```

首先遍历种子文件收集初始分数，然后调用`SeedSchedule`进行种子调度，并根据游戏分数对种子进行能量分配，最后调用`MutatorSchedule`进行变异算子调度，并对变异后返回结果分析进行对应的保存。

```python
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
```

#### Transform

> transform.py

使用枚举规定Transform种类，除规定实现的CharFlip, CharIns, CharDel, Havoc, Splice五种算子，增加Shuffle变异算子：

```python
class TransformKind(Enum):
    """Transforms for the action."""
    CHAR_FLIP = 0
    CHAR_INS = 1
    CHAR_DEL = 2
    HAVOC = 3
    SPLICE = 4
    SHUFFLE = 5
```

新增的Shuffle变异算子：对操作序列本身乱序

```python
def shuffle(self):
    self.input_data = ''.join(random.sample(self.input_data, len(self.input_data)))
    return self.input_data
```

#### Run

> run.py

// TODO

### Utilities

#### PreProcess

> preprocess/

// TODO

#### Output Analyzer

> output_analysis/

// TODO

#### Mutator Scheduler

> mutator_schedule/

// TODO

#### Seed Scheduler

> seed_schedule/

// TODO