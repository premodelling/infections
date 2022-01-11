import glob
import os

import dask
import pandas as pd


class AgeGroupSexLTLA:

    def __init__(self):
        """
        Constructor
        """

        # population data set
        sources_path = os.path.join(os.getcwd(), 'warehouse', 'populations', 'msoa', 'group')
        self.sources = glob.glob(pathname=os.path.join(sources_path, '*.csv'))

        # storage
        self.storage = os.path.join(os.getcwd(), 'warehouse', 'populations', 'ltla', 'group')
        self.__path()

    def __path(self):
        """
        Ascertains the existence of warehouse/populations/single

        :return:
        """

        if not os.path.exists(self.storage):
            os.makedirs(self.storage)

    @dask.delayed
    def __population(self, source: str) -> pd.DataFrame:
        """

        :param source:
        :return:
        """

        try:
            population = pd.read_csv(filepath_or_buffer=source, header=0, encoding='utf-8')
        except RuntimeError as err:
            raise Exception(err)

        return population

    @dask.delayed
    def __aggregates(self, population: pd.DataFrame) -> pd.DataFrame:
        """

        :param population:
        :return:
        """

        aggregates = population.drop(columns='msoa').groupby(by=['ltla', 'sex']).agg('sum')
        aggregates.reset_index(drop=False, inplace=True)

        return aggregates

    @dask.delayed
    def __write(self, frame: pd.DataFrame, filename: str) -> str:
        """

        :param frame:
        :param filename:
        :return:
        """

        try:
            frame.to_csv(path_or_buf=os.path.join(self.storage, filename),
                         index=False, header=True, encoding='utf-8')
            return '{}: succeeded'.format(filename.split('.')[0])
        except RuntimeError as err:
            raise Exception(err)

    def exc(self) -> list:
        """

        :return:
        """

        # read & process the data sets in parallel
        computations = []
        for source in self.sources:

            population = self.__population(source=source)
            aggregates = self.__aggregates(population=population)
            message = self.__write(frame=aggregates, filename=os.path.basename(source))

            computations.append(message)

        dask.visualize(computations, filename='ageGroupsLTLA', format='pdf')
        messages = dask.compute(computations, scheduler='processes')[0]

        return messages
