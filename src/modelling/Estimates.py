import collections
import os

import pandas as pd

import src.modelling.EstimatesCNN
import src.modelling.EstimatesLSTM
import src.modelling.ModellingSteps
import src.modelling.WindowGenerator


class Estimates:

    def __init__(self, n_features: int, output_steps: int):
        """

        :param n_features:
        :param output_steps:
        """

        self.n_features = n_features
        self.output_steps = output_steps

        self.steps = src.modelling.ModellingSteps.ModellingSteps()

        self.storage = os.path.join(os.getcwd(), 'warehouse', 'modelling', 'evaluations', 'histories')

    @staticmethod
    def __path(path: str):
        """

        :param path:
        :return:
        """

        if not os.path.exists(path):
            os.makedirs(path)

    def __write(self, blob: pd.DataFrame, method: str, width: int):
        """

        :param blob:
        :param method:
        :param width:
        :return:
        """

        try:
            blob.to_csv(path_or_buf=os.path.join(self.storage, method, '{:03d}.csv'.format(width)),
                        index=False, header=True)
        except RuntimeError as err:
            raise Exception(err)

    def __convolution(self, width: int, window: src.modelling.WindowGenerator.WindowGenerator):
        """

        :param width:
        :param window:
        :return:
        """

        convolution_, method = src.modelling.EstimatesCNN.EstimatesCNN(
            n_features=self.n_features, output_steps=self.output_steps).exc(width=width, window=window)

        return convolution_, method

    def __lstm(self, width: int, window: src.modelling.WindowGenerator.WindowGenerator):
        """

        :param width:
        :param window:
        :return:
        """

        lstm_, method = src.modelling.EstimatesLSTM.EstimatesLSTM(
            n_features=self.n_features, output_steps=self.output_steps).exc(width=width, window=window)

        return lstm_, method

    def exc(self, widths: range, arguments: collections.namedtuple(typename='Arguments',
                                                                   field_names=['input_width', 'label_width', 'shift',
                                                                                'training_', 'validating_', 'testing_',
                                                                                'label_columns'])):
        """

        :param widths:
        :param arguments:
        :return:
        """

        validations = pd.DataFrame(columns=['method', 'history', 'ahead', 'loss', 'mae'])
        tests = pd.DataFrame(columns=['method', 'history', 'ahead', 'loss', 'mae'])

        for width in widths:

            # latest window instance, optimise this segment
            window = src.modelling.WindowGenerator.WindowGenerator(
                input_width=width, label_width=arguments.label_width, shift=arguments.shift,
                training=arguments.training_, validating=arguments.validating_, testing=arguments.testing_,
                label_columns=arguments.label_columns)

            # CNN Modelling
            convolution_, method = self.__convolution(width=width, window=window)
            validations.loc[validations.shape[0], :] = [method, width, self.output_steps] + convolution_.model.evaluate(
                window.validate, verbose=0)
            tests.loc[tests.shape[0], :] = [method, width, self.output_steps] + convolution_.model.evaluate(window.test,
                                                                                                            verbose=0)
            # LSTM Modelling
            lstm_, method = self.__lstm(width=width, window=window)
            validations.loc[validations.shape[0], :] = [method, width, self.output_steps] + lstm_.model.evaluate(
                window.validate, verbose=0)
            tests.loc[tests.shape[0], :] = [method, width, self.output_steps] + lstm_.model.evaluate(window.test,
                                                                                                     verbose=0)

        return validations, tests
