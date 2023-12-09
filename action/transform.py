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


class Transform:
    """Transforms for the action."""

    def __init__(self, input_data):
        self.input_data = input_data

    def transform(self):
        action_kind = random.choice(list(TransformKind))
        return self.take_action(action_kind)

    def take_action(self, transform_kind):
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

    def char_flip(self, n=1, L=1, S=1):
        logging.info(f"Running transform char flip with input_data: {self.input_data}")
        for _ in range(min(L, len(self.input_data) // S)):
            start = random.randint(0, len(self.input_data) - S)
            end = start + S
            self.input_data = (
                self.input_data[:start] + self.input_data[start:end][::-1] + self.input_data[end:]
            )
        return self.input_data

    def char_ins(self, n=1, K=1):
        logging.info(f"Running transform char insert with input_data: {self.input_data}")
        for _ in range(n):
            position = random.randint(0, len(self.input_data))
            chars_to_insert = ''.join(random.choice('aslrd') for _ in range(K))
            self.input_data = self.input_data[:position] + chars_to_insert + self.input_data[position:]
        return self.input_data

    def char_del(self, n=1, K=1):
        logging.info(f"Running transform char delete with input_data: {self.input_data}")
        for _ in range(n):
            if len(self.input_data) > K:
                position = random.randint(0, len(self.input_data) - K)
                self.input_data = self.input_data[:position] + self.input_data[position + K:]
        return self.input_data

    def havoc(self, num_transforms=1):
        logging.info(f"Running transform havoc with input_data: {self.input_data}")
        for _ in range(num_transforms):
            transform_kind = random.choice([TransformKind.CHAR_FLIP, TransformKind.CHAR_INS, TransformKind.CHAR_DEL])
            self.take_action(transform_kind)
        return self.input_data

    def splice(self):
        logging.info(f"Running transform splice with input_data: {self.input_data}")
        midpoint = len(self.input_data) // 2
        self.input_data = self.input_data[midpoint:] + self.input_data[:midpoint]
        return self.input_data
