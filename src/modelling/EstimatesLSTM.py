import os

import tensorflow as tf

import pandas as pd

import src.modelling.ModellingSteps
import src.modelling.WindowGenerator

os.environ["CUDA_VISIBLE_DEVICES"] = "-1"


class EstimatesLSTM:

    def __init__(self, n_features: int, output_steps: int):
        """

        :param n_features:
        :param output_steps:
        """

        self.n_features = n_features
        self.output_steps = output_steps

        self.steps = src.modelling.ModellingSteps.ModellingSteps()

        self.method = 'LSTM'

        self.storage = os.path.join(os.getcwd(), 'warehouse', 'modelling', 'evaluations', 'histories', self.method)
        self.__path()

    def __path(self):

        if not os.path.exists(self.storage):
            os.makedirs(self.storage)

    def __write(self, blob: pd.DataFrame, width: int):
        """

        :param blob:
        :param width:
        :return:
        """

        try:
            blob.to_csv(path_or_buf=os.path.join(self.storage, '{:03d}.csv'.format(width)),
                        index=False, header=True)
        except RuntimeError as err:
            raise Exception(err)

    def exc(self, width: int, window: src.modelling.WindowGenerator.WindowGenerator):
        """

        :param width:
        :param window:
        :return:
        """

        lstm = tf.keras.Sequential([
            tf.keras.layers.LSTM(32, return_sequences=False),
            tf.keras.layers.Dense(self.output_steps * self.n_features, kernel_initializer=tf.initializers.zeros()),
            tf.keras.layers.Reshape([self.output_steps, self.n_features])
        ])

        lstm_ = self.steps.modelling(model=lstm, window=window)

        lstm_history = pd.DataFrame(data=lstm_.history)
        lstm_history.loc[:, 'method'] = self.method
        lstm_history.loc[:, 'history'] = width
        lstm_history.loc[:, 'ahead'] = self.output_steps

        self.__write(blob=lstm_history, width=width)

        return lstm_, self.method
