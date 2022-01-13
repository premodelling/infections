import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


class DataNormalisation:

    def __init__(self, training: pd.DataFrame, validating: pd.DataFrame, testing: pd.DataFrame):
        """

        """

        self.__training = training
        self.__validating = validating
        self.__testing = testing

        self.__mean = self.__training.mean()
        self.__deviation = self.__training.std()

    def __normalise(self, data: pd.DataFrame):

        return (data - self.__mean) / self.__deviation

    def graph(self, data):

        normalised = self.__normalise(data)
        melted = normalised.melt(var_name='Field', value_name='Normalised')

        plt.figure(figsize=(13, 3.5))
        sns.axes_style('white')

        handle = sns.violinplot(x='Field', y='Normalised', data=melted)
        sns.despine(offset=10, trim=True)
        handle.set_xticklabels(normalised.keys(), rotation=90)

    def exc(self):
        
        training = self.__normalise(data=self.__training)
        validating = self.__normalise(data=self.__validating)
        testing = self.__normalise(data=self.__testing)

        return training, validating, testing
