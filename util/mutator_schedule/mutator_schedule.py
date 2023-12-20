import math

# 假设这是你的游戏评分函数
import numpy as np
import action
from action.transform import Transform
from tqdm import tqdm


def get_score(seed, energy):
    is_mario, _, score = action.run.play_game(seed, energy)
    return is_mario, score


class MutatorSchedule:
    def __init__(self, seed_score_pairs, energy, temperature=1.0, cooling_rate=0.95, iterations=10):
        self.seed_score_pairs = seed_score_pairs
        self.energy = energy
        self.temperature = temperature
        self.cooling_rate = cooling_rate
        self.iterations = iterations

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
