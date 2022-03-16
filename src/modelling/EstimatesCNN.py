import collections
import os

import pandas as pd
import tensorflow as tf

import src.modelling.ModellingSteps
import src.modelling.WindowGenerator
import src.utilities.directories

os.environ["CUDA_VISIBLE_DEVICES"] = "-1"


class EstimatesCNN:

    def __init__(self, n_features: int, output_steps: int):
        """

        :param n_features:
        :param output_steps:
        """

        self.n_features = n_features
        self.output_steps = output_steps

        # an instance of modelling steps
        self.steps = src.modelling.ModellingSteps.ModellingSteps()

        # method
        self.method = 'CNN'

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

        convolution = tf.keras.Sequential([
            tf.keras.layers.Lambda(lambda x: x[:, -width:, :]),
            tf.keras.layers.Conv1D(256, activation='relu', kernel_size=width),
            tf.keras.layers.Dense(self.output_steps * self.n_features, kernel_initializer=tf.initializers.zeros()),
            tf.keras.layers.Reshape([self.output_steps, self.n_features])
        ])

        convolution_ = self.steps.modelling(model=convolution, window=window)

        convolution_history = pd.DataFrame(convolution_.history)
        convolution_history.loc[:, 'method'] = self.method
        convolution_history.loc[:, 'history'] = width
        convolution_history.loc[:, 'ahead'] = self.output_steps

        self.__write(blob=convolution_history, width=width)

        return convolution_, self.__diagnostics(width=width, window=window, model_=convolution_)
