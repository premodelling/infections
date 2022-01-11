import pandas as pd
import os.path


class Populations:

    def __init__(self, source_path):
        """

        :param source_path:
        """

        self.source_path = source_path

    def __aggregates(self, frame: pd.DataFrame) -> pd.DataFrame:
        """
        Calculates the population of each MSOA, and each LTLA.  Each LTLA consist of
        one or more MSOA geographic entities; a MSOA is a member of a single LTLA only.

        MSOA: Middle Super Output Area
        LTLA: Lower Tier Local Authority

        :param frame:
        :return:
        """

        # MSOA populations
        edges = frame.copy().drop(columns='sex').groupby(by=['msoa', 'ltla']).agg('sum').sum(axis=1)
        edges.rename('ppln_msoa', inplace=True)
        edges = edges.to_frame().reset_index(drop=False)

        # LTLA populations
        nodes = edges.copy().drop(columns='msoa').groupby(by='ltla').agg(ppln_ltla=('ppln_msoa', sum))
        nodes.reset_index(drop=False, inplace=True)

        # merge
        aggregates = edges.merge(nodes, how='left', on='ltla')

        return aggregates

    def __read(self, filename: str) -> pd.DataFrame:
        """
        Reads a population data set

        :param filename:
        :return:
        """

        try:
            frame = pd.read_csv(filepath_or_buffer=os.path.join(self.source_path, filename), header=0, encoding='utf-8')
        except RuntimeError as err:
            raise Exception(err)

        return frame

    def exc(self, filename: str):
        """

        :param filename:
        :return:
        """

        # population data; the data consists of population numbers per labelled
        # age group & sex intersection of a middle super output area (MSOA)
        population = self.__read(filename=filename)

        # calculates higher level population values
        aggregates = self.__aggregates(frame=population)

        # appends the aggregates to the population table
        population = population.merge(aggregates, how='left', on=['msoa', 'ltla'])

        return population
