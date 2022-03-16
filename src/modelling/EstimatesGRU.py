import collections
import os

import pandas as pd
import tensorflow as tf

import src.modelling.ModellingSteps
import src.modelling.WindowGenerator
import src.utilities.directories

os.environ["CUDA_VISIBLE_DEVICES"] = "-1"


class EstimatesGRU:

    def __init__(self, n_features: int, output_steps: int):
        """

        :param n_features:
        :param output_steps:
        """

        self.n_features = n_features
        self.output_steps = output_steps

        # an instance of modelling steps
        # trial mode, hence the low number of epochs
        self.steps = src.modelling.ModellingSteps.ModellingSteps(epochs=5)

        # method
        self.method = 'GRU'

        # storage
        self.storage = os.path.join(os.getcwd(), 'warehouse', 'modelling', 'evaluations', 'histories', self.method)
        self.__path()

    def __path(self):

        src.utilities.directories.Directories().create(text=self.storage)

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

    def __diagnostics(self, width: int, window: src.modelling.WindowGenerator.WindowGenerator,
                      model_: tf.keras.Model):

        Diagnostics = collections.namedtuple(typename='Diagnostics', field_names=['validations', 'tests'])

        diagnostics = Diagnostics(
            validations=[self.method, width, self.output_steps] + model_.model.evaluate(window.validate, verbose=0),
            tests=[self.method, width, self.output_steps] + model_.model.evaluate(window.test, verbose=0))

        return diagnostics

    def exc(self, width: int, window: src.modelling.WindowGenerator.WindowGenerator):
        """

        :param width:
        :param window:
        :return:
        """

        gru = tf.keras.Sequential([
            tf.keras.layers.GRU(32, input_shape=(width, self.n_features), return_sequences=True, activation='relu',
                                kernel_initializer=tf.initializers.HeUniform()),
            tf.keras.layers.Dropout(0.1),
            tf.keras.layers.GRU(16, return_sequences=True, activation='relu'),
            tf.keras.layers.Dropout(0.1),
            tf.keras.layers.GRU(self.output_steps * self.n_features, activation='relu'),
            tf.keras.layers.Reshape([self.output_steps, self.n_features])
        ])

        gru_ = self.steps.modelling(model=gru, window=window)

        gru_history = pd.DataFrame(data=gru_.history)
        gru_history.loc[:, 'method'] = self.method
        gru_history.loc[:, 'history'] = width
        gru_history.loc[:, 'ahead'] = self.output_steps

        self.__write(blob=gru_history, width=width)

        return gru_, self.__diagnostics(width=width, window=window, model_=gru_)
