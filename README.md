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

Game: [Mario-Level-1](https://github.com/cardigan1008/Mario-Level-1)

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
4. 测试生成：六种变异算子，并使用退火算法进行变异算子调度
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

使用pynput库将字符串的操作序列转换为游戏中的输入

```python
class KeyboardActions:
    def __init__(self):
        self.keyboard = Controller()
        self.time_interval = 0.5

    def press_a_key(self):
        self.keyboard.press('a')
        time.sleep(self.time_interval)
        self.keyboard.release('a')
    def press_up_key(self):
        self.keyboard.press(Key.up)
        time.sleep(self.time_interval)
        self.keyboard.release(Key.up)
    def press_s_key(self):
        self.keyboard.press('s')
        time.sleep(self.time_interval)
        self.keyboard.release('s')

    def press_left_key(self):
        self.keyboard.press(Key.left)
        time.sleep(self.time_interval)
        self.keyboard.release(Key.left)

    def press_right_key(self):
        self.keyboard.press(Key.right)
        time.sleep(self.time_interval)
        self.keyboard.release(Key.right)

    def press_down_key(self):
        self.keyboard.press(Key.down)
        time.sleep(self.time_interval)
        self.keyboard.release(Key.down)

    def press_enter_key(self):
        self.keyboard.press(Key.enter)
        time.sleep(self.time_interval)
        self.keyboard.release(Key.enter)
```

对游戏窗口截图，交由识别部分进行图像识别，实时得到结果

```python
def take_screenshot(window):
    # 获取窗口位置和大小
    window_x, window_y, window_width, window_height = window.left, window.top, window.width, window.height

    # 截取窗口图像
    screenshot = pyautogui.screenshot(region=(window_x + 20, window_y, window_width - 20, window_height - 20))
    # 将Pillow图像对象转换为OpenCV图像对象
    opencv_image = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    # 将OpenCV图像对象转换为灰度图像
    gray_image = cv2.cvtColor(opencv_image, cv2.COLOR_BGR2GRAY)
    boolValue = analysis.check_image(gray_image)
    gold = analysis.extract_gold(opencv_image)
    score = analysis.extract_score(opencv_image)

    # 可以根据需要返回截图对象或者其他信息
    return boolValue, gold, score
```

创建游戏进程，开始游戏操作

```python
    pygame_process = subprocess.Popen(['python', game_path + '/mario_level_1.py'], stdin=subprocess.PIPE)
```

### Utilities

#### PreProcess

> preprocess/

##### Mario

> mario/

存储三种状态下的mario图像素材

##### Resources

> resources/

存储原始的mario游戏素材

> getMarioPics.py

对原始mario游戏素材进行切片，得到三种状态下的mario图像素材

```python
def main():
    mario_sprites = MarioSprites()

    # 保存所有图片
    save_images(mario_sprites.right_frames, "./mario/small_normal", "right_small_normal")
    save_images(mario_sprites.left_frames, "./mario/small_normal", "left_small_normal")

    save_images(mario_sprites.left_big_normal_frames, "./mario/big_normal", "left_big_normal")
    save_images(mario_sprites.right_big_normal_frames,"./mario/big_normal", "right_big_normal")

    save_images(mario_sprites.right_fire_frames, "./mario/big_fire", "right_big_fire")
```

#### Output Analyzer

> output_analysis/

##### NumberTrain

> numberTrain.py

对游戏的数字图像进行训练，通过图像中的数字轮廓，将每个数字提取出来，并将这些数字的分类结果和压平图像分别保存到 classifications.txt 和 flattened_images.txt中。

```python
 # 遍历所有轮廓
 for npaContour in npaContours:
     # 如果轮廓面积大于阈值
     if cv2.contourArea(npaContour) > MIN_CONTOUR_AREA:
         [intX, intY, intW, intH] = cv2.boundingRect(npaContour)

         # 在原始图像上绘制红色矩形
         cv2.rectangle(imgTrainingNumbers, (intX, intY), (intX + intW, intY + intH), (0, 0, 255), 2)

         imgROI = imgThresh[intY:intY + intH, intX:intX + intW]
         imgROIResized = cv2.resize(imgROI, (RESIZED_IMAGE_WIDTH, RESIZED_IMAGE_HEIGHT))

         # 显示原始字符区域和调整大小后的字符区域
         cv2.imshow("imgROI", imgROI)
         cv2.imshow("imgROIResized", imgROIResized)
         cv2.imshow("training_numbers.png", imgTrainingNumbers)

         # 获取键盘输入
         intChar = cv2.waitKey(0)

         # 如果按下ESC键，退出程序
         if intChar == 27:
             sys.exit()
         # 如果按下有效字符，添加到分类列表
         elif intChar in intValidChars:
             intClassifications.append(intChar)

             # 压平字符区域并添加到数组
             npaFlattenedImage = imgROIResized.reshape((1, RESIZED_IMAGE_WIDTH * RESIZED_IMAGE_HEIGHT))
             npaFlattenedImages = np.append(npaFlattenedImages, npaFlattenedImage, 0)

 fltClassifications = np.array(intClassifications, np.float32)
 npaClassifications = fltClassifications.reshape((fltClassifications.size, 1))

 print("\n训练完成！！\n")
 np.savetxt("classifications.txt", npaClassifications)
 np.savetxt("flattened_images.txt", npaFlattenedImages)
```

##### NumberExtract

> numberExtract.py

通过训练好的KNN模型对输入的数字图像进行识别提取。

```python
def number_get(test_image):
  
    ......
    
    # 创建KNN对象
    kNearest = cv2.ml.KNearest_create()

    # 训练KNN模型
    kNearest.train(npaFlattenedImages, cv2.ml.ROW_SAMPLE, npaClassifications)

    ......
    
    # 最终识别结果字符串
    strFinalString = ""

    # 遍历有效轮廓
    for contourWithData in validContoursWithData:
        # 获取数字区域
        imgROI = imgThresh[contourWithData.intRectY: contourWithData.intRectY + contourWithData.intRectHeight,
                 contourWithData.intRectX: contourWithData.intRectX + contourWithData.intRectWidth]

        # 调整数字区域大小
        imgROIResized = cv2.resize(imgROI, (RESIZED_IMAGE_WIDTH, RESIZED_IMAGE_HEIGHT))

        # 将数字区域展平为一维numpy数组
        npaROIResized = imgROIResized.reshape((1, RESIZED_IMAGE_WIDTH * RESIZED_IMAGE_HEIGHT))

        # 将数据类型转换为float32
        npaROIResized = np.float32(npaROIResized)

        # 使用KNN进行识别
        retval, npaResults, neigh_resp, dists = kNearest.findNearest(npaROIResized, k=1)

        # 获取识别结果字符
        strCurrentChar = str(chr(int(npaResults[0][0])))
        strFinalString = strFinalString + strCurrentChar
    return strFinalString
```

##### OutputAnalysis

> outputAnalysis.py

提取mario图像的特征点，将特征点保存在train_des.pkl

```python
def extract_mario_des(self):
    template_image_path = '../preprocess/mario/small_normal/right_small_normal_0.png'
    arr_des = []
    arr_kp = []
    arr_template = []
    # 遍历文件
    PATH_TO_TEST_IMAGES_DIR = '../preprocess/mario'
    for pidImage in glob.glob(PATH_TO_TEST_IMAGES_DIR + "/*/*.png"):
        template_image_path = pidImage
        template_image_path = template_image_path.replace('\\', '/')
        # print(template_image_path)

        # 读取mario和背景
        template = cv2.imread(template_image_path, 0)
        if template is None:
            print('Could not open or find the images!')
            exit(0)
        template = cv2.resize(template, None, fx=2, fy=2)
        # 创建SIFT对象
        sift = cv2.xfeatures2d.SIFT_create()
        # 提取特征点
        kp1, des1 = sift.detectAndCompute(template, None)
        arr_des.append(des1)
        arr_kp.append(kp1)
        arr_template.append(template)
    save_data('train_des.pkl', arr_des)
    return arr_des, arr_kp, arr_template
```

提取游戏窗口截图的特征点，与已提取的mario特征点进行匹配，返回输入图像中是否包含mario
```python
def check_image(self, screenshot):
    train_des = load_des('train_des.pkl')
    if screenshot is None:
        print('Could not open or find the images!')
        exit(0)
    # 创建SIFT对象
    sift = cv2.SIFT_create()
    # 提取特征点
    kp2, des2 = sift.detectAndCompute(screenshot, None)
    bf = cv2.BFMatcher()
    for i in range(len(train_des)):
        # 匹配特征点
        matches = bf.knnMatch(train_des[i], des2, k=2)
        good = []
        for m, n in matches:
            if m.distance < 0.75 * n.distance:
                good.append([m])
        # 若匹配超过3点则认为存在
        if len(good) > 3:
            return True
    return False
```

提取游戏窗口截图中的游戏分数

```python
def extract_score(self, screen):
    imgROI = screen[165:219, 140:429]
    # cv2.imshow("ROI_WIN", imgROI)
    # cv2.waitKey(0)
    res = number_get(imgROI)
    if len(res) > 6:
        res = res[0:6]
    # print("score:"+res)
    return res
```

提取游戏窗口截图中的金币数

```python
def extract_gold(self, screen):
    imgROI = screen[165:219, 635:730]
    # cv2.imshow("ROI_WIN", imgROI)
    # cv2.waitKey(0)
    res = number_get(imgROI)
    if len(res) > 2:
        res = res[0:2]
    # print("gold:"+res)
    return res
```

#### Mutator Scheduler

> mutator_schedule/

实现了一个可以根据种子和能量进行游戏运行的函数。
```python
def get_score(seed, energy):
    is_mario, _, score = action.run.play_game(seed, energy)
    return is_mario, score
```
以模拟退火算法为载体进行变异调度，先选中操作种子，并获取其得分。如果发生崩溃，停止操作并返回崩溃。在算法中，通过在迭代循环中在当前种子附近进行变异，并计算新种子的得分，同时监测程序是否崩溃，然后根据Metropolis准则计算接受概率，在接受概率内或得到了更高分的种子-得分对的情况下，会更新种子-得分对，循环直到迭代结束。最后函数会返回迭代完成后的最佳种子-得分对。
```python
def schedule(self):
    current_op = self.seed_score_pairs[0]
    is_mario, current_score = get_score(current_op, len(current_op))

    if not is_mario:
        return current_op, current_score, False

    best_op = current_op
    best_score = current_score

    for _ in tqdm(range(self.iterations)):
        self.temperature *= self.cooling_rate

        # 在当前字符串附近进行变化
        transform_action = Transform(current_op)
        new_op = transform_action.transform()

        # 计算新字符串的得分
        is_mario, new_score = get_score(new_op, self.energy)

        if not is_mario:
            return new_op, current_score, False

        # 计算接受概率
        acceptance_probability = math.exp((new_score - current_score) / self.temperature)

        # 根据概率决定是否接受新字符串
        if new_score > current_score or np.random.uniform(low=0, high=1) < acceptance_probability:
            current_op = new_op
            current_score = new_score

        # 更新最佳字符串
        if current_score > best_score:
            best_op = current_op
            best_score = current_score

    return best_op, best_score, True
```
#### Seed Scheduler

> seed_schedule/

实现了一个排序算法，用于对种子序列进行排序。
```python
def sort_tuples(tuples_list):
    sorted_tuples = sorted(tuples_list, key=lambda x: x[1], reverse=True)
    return sorted_tuples
```
实现了一个选择算法，用于对种子进行有一定权重的选择。在这里，我们将排好序的种子-分数对按一定比例切分成高分组和低分组，并在低分组中随机选取一个同高分数组一同进行随机选择。
```python
def select_tuples(sorted_tuples, high_ratio):
    total_tuples = len(sorted_tuples)
    high_count = int(total_tuples * high_ratio)

    high_tuples = sorted_tuples[:high_count]
    random_tuple = random.choice(sorted_tuples[high_count:])

    selected_tuple = random.choice(high_tuples + [random_tuple])
    return selected_tuple
```

