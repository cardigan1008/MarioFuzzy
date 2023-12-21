import logging
import random
from enum import Enum


class TransformKind(Enum):
    """Transforms for the action."""
    CHAR_FLIP = 0
    CHAR_INS = 1
    CHAR_DEL = 2
    HAVOC = 3
    SPLICE = 4
    SHUFFLE = 5


class Transform:
    """Transforms for the action."""

    def __init__(self, input_data):
        self.input_data = input_data

    def transform(self):
        action_kind = random.choice(list(TransformKind))
        # action_kind = TransformKind.CHAR_INS
        return self.take_action(action_kind)

    def take_action(self, transform_kind):
        logging.info(f"Running transform {transform_kind}...")
        if transform_kind == TransformKind.CHAR_FLIP:
            return self.char_flip()
        elif transform_kind == TransformKind.CHAR_INS:
            return self.char_ins()
        elif transform_kind == TransformKind.CHAR_DEL:
            return self.char_del()
        elif transform_kind == TransformKind.HAVOC:
            return self.havoc()
        elif transform_kind == TransformKind.SPLICE:
            return self.splice()
        elif transform_kind == TransformKind.SHUFFLE:
            return self.shuffle()

    def char_flip(self, n=None, K=None):
        K = random.randint(1, len(self.input_data)) if K is None else min(K, len(self.input_data))
        n = random.randint(0, len(self.input_data)) if n is None else min(n, len(self.input_data))

        cur_data = self.input_data + self.input_data[0:n]

        for _ in range(len(cur_data) // K):
            start = random.randint(0, len(self.input_data) - K)
            end = start + K
            self.input_data = (
                self.input_data[:start] + self.input_data[start:end][::-1] + self.input_data[end:]
            )
        return cur_data[0:len(self.input_data)]

    def char_ins(self, n=None, K=None):
        # 随机化参数，但确保不超过限制
        n = random.randint(1, len(self.input_data)) if n is None else min(n, len(self.input_data))
        K = random.randint(1, len(self.input_data)) if K is None else min(K, len(self.input_data))

        for _ in range(n):
            position = random.randint(0, len(self.input_data))
            chars_to_insert = ''.join(random.choice('aslrd') for _ in range(K))
            self.input_data = self.input_data[:position] + chars_to_insert + self.input_data[position:]
        return self.input_data

    def char_del(self, n=None, K=None):
        # 随机化参数，但确保不超过限制
        n = random.randint(1, len(self.input_data)) if n is None else min(n, len(self.input_data))
        K = random.randint(1, len(self.input_data)) if K is None else min(K, len(self.input_data))

        for _ in range(n):
            if len(self.input_data) > K:
                position = random.randint(0, len(self.input_data) - K)
                self.input_data = self.input_data[:position] + self.input_data[position + K:]
        return self.input_data

    def havoc(self, num_transforms=None):
        # 随机化参数，但确保不超过限制
        num_transforms = random.randint(1, 3) if num_transforms is None else min(num_transforms, 3)

        for _ in range(num_transforms):
            transform_kind = random.choice([TransformKind.CHAR_FLIP, TransformKind.CHAR_INS, TransformKind.CHAR_DEL])
            self.take_action(transform_kind)
        return self.input_data

    def splice(self):
        midpoint = len(self.input_data) // 2
        self.input_data = self.input_data[midpoint:] + self.input_data[:midpoint]
        return self.input_data

    def shuffle(self):
        self.input_data = ''.join(random.sample(self.input_data, len(self.input_data)))
        return self.input_data
