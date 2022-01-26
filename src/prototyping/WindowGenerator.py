import numpy as np
import pandas as pd

import tensorflow as tf


class WindowGenerator:
    def __init__(self, input_width: int, label_width: int, shift: int,
                 training: pd.DataFrame, validating: pd.DataFrame, testing: pd.DataFrame,
                 label_columns: list = None):
        
        # data
        self.training = training
        self.validating = validating
        self.testing = testing

        # the label field/s
        self.label_columns = label_columns
        if self.label_columns is not None:
            self.label_columns_indices = {name: i for i, name in enumerate(self.label_columns)}

        # all fields
        self.column_indices = {name: i for i, name in enumerate(training.columns)}

        # window parameters
        self.input_width = input_width
        self.label_width = label_width
        self.shift = shift
        self.total_window_size = input_width + shift

        # input slice
        self.input_slice = slice(0, input_width)
        self.input_indices = np.arange(self.total_window_size)[self.input_slice]
        self.label_start = self.total_window_size - self.label_width
        self.label_slice = slice(self.label_start, None)
        self.label_indices = np.arange(self.total_window_size)[self.label_slice]

    def split_window(self, features):

        inputs = features[:, self.input_slice, :]
        labels = features[:, self.label_slice, :]
        if self.label_columns is not None:
            labels = tf.stack(
                [labels[:, :, self.column_indices[name]] for name in self.label_columns],
                axis=-1)

        # Herein, the shapes are manually set because slicing does not preserve static shape information; due to this
        # set-up the inspection of `tf.data.Datasets` objects should be straightforward.
        inputs.set_shape([None, self.input_width, None])
        labels.set_shape([None, self.label_width, None])

        return inputs, labels

    def make_dataset(self, data):

        data = np.array(data, dtype=np.float32)

        # noinspection PyUnresolvedReferences
        dataset = tf.keras.preprocessing.timeseries_dataset_from_array(
            data=data, targets=None, sequence_length=self.total_window_size,
            sequence_stride=1, shuffle=False, batch_size=32)

        dataset = dataset.map(self.split_window)

        return dataset

    @property
    def train(self):
        return self.make_dataset(self.training)

    @property
    def validate(self):
        return self.make_dataset(self.validating)

    @property
    def test(self):
        return self.make_dataset(self.testing)

    @property
    def example(self):

        sample = getattr(self, '_example', None)
        if sample is None:
            sample = next(iter(self.train))

        return sample

    def __repr__(self):
        return '\n'.join([
            f'Total window size: {self.total_window_size}',
            f'Input indices: {self.input_indices}',
            f'Label indices: {self.label_indices}',
            f'Label column name(s): {self.label_columns}'])
