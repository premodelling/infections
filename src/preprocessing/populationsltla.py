"""
Calculates the population of each lower tier local authority (LTLA) by age & sex
"""
import os
import glob

import dask
import pandas as pd


class PopulationsLTLA:

    def __init__(self):
        """
        Constructor
        """

        # the latest districts data
        self.districts_file = os.path.join(os.getcwd(), 'warehouse', 'geography', 'districts', '2020.csv')
        self.districts = self.__districts()

        # population data set
        sources_path = os.path.join(os.getcwd(), 'warehouse', 'populations', 'msoa', 'single')
        self.sources = glob.glob(pathname=os.path.join(sources_path, '*.csv'))

        # storage
        self.storage = os.path.join(os.getcwd(), 'warehouse', 'populations', 'ltla', 'single')
        self.__path()

    def __path(self):
        """
        Ascertains the existence of warehouse/populations/single

        :return:
        """

        if not os.path.exists(self.storage):
            os.makedirs(self.storage)

    def __districts(self) -> pd.DataFrame:
        """

        :return:
        """

        try:
            districts = pd.read_csv(filepath_or_buffer=self.districts_file, header=0,
                                    encoding='utf-8', usecols=['MSOA11CD', 'LAD20CD'])
        except RuntimeError as err:
            raise Exception(err)

        districts.rename({'MSOA11CD': 'msoa', 'LAD20CD': 'ltla'}, axis=1, inplace=True)

        return districts

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

        frame = population.merge(self.districts, how='left', on='msoa')
        aggregates = frame.drop(columns='msoa').groupby(by=['ltla', 'sex']).agg('sum')
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

        computations = []
        for source in self.sources:

            population = self.__population(source=source)
            aggregates = self.__aggregates(population=population)
            message = self.__write(frame=aggregates, filename=os.path.basename(source))

            computations.append(message)

        dask.visualize(computations, filename='populationsLTLA', format='pdf')
        messages = dask.compute(computations, scheduler='processes')[0]

        return messages
