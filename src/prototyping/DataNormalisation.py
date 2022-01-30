import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


class DataNormalisation:

    def __init__(self, training: pd.DataFrame, validating: pd.DataFrame, testing: pd.DataFrame):
        """

        :param training:
        :param validating:
        :param testing:
        """

        self.__training = training
        self.__validating = validating
        self.__testing = testing

        self.__mean = self.__training.mean(axis=0)
        self.__deviation = self.__training.std(axis=0)

    def __normalise(self, data: pd.DataFrame):
        """

        :param data:
        :return:
        """

        return (data - self.__mean) / self.__deviation

    def graph(self, data):
        """

        :param data:
        :return:
        """

        normalised = self.__normalise(data)
        melted = normalised.melt(var_name='Field', value_name='Normalised')

        plt.figure(figsize=(13, 3.5))
        sns.axes_style('white')

        handle = sns.violinplot(x='Field', y='Normalised', data=melted)
        sns.despine(offset=10, trim=True)
        handle.set_xticklabels(normalised.keys(), rotation=90)

    def exc(self):
        """

        :return:
        """
        
        training = self.__normalise(data=self.__training)
        validating = self.__normalise(data=self.__validating)
        testing = self.__normalise(data=self.__testing)

        return training, validating, testing
