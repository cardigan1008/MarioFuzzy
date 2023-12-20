import random
import math

# 假设这是你的游戏评分函数
import numpy as np
import action
from action.transform import Transform
from tqdm import tqdm


def get_score(seed):
    return random.random()
    # 在这里计算单次游戏得分

def simulated_annealing_optimization(initial_string, temperature=1.0, cooling_rate=0.95, iterations=1000):
    current_string = initial_string
    current_score = get_score(current_string)

    best_string = current_string
    best_score = current_score

    for i in tqdm(range(iterations)):
        temperature *= cooling_rate

        # 在当前字符串附近进行变化
        new_string = Transform.transform(current_string)

        # 计算新字符串的得分
        new_score = get_score(new_string)

        # 计算接受概率
        acceptance_probability = math.exp((new_score - current_score) / temperature)

        # 根据概率决定是否接受新字符串
        if new_score > current_score or np.random.uniform(low=0, high=1) < acceptance_probability:
            current_string = new_string
            current_score = new_score

        # 更新最佳字符串
        if current_score > best_score:
            best_string = current_string
            best_score = current_score

    return best_string, best_score
