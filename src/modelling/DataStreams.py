import collections
import glob
import os
import pathlib

import dask
import numpy as np
import pandas as pd

import config
import src.modelling.DataSplitting


class DataStreams:

    def __init__(self, fraction: collections.namedtuple(typename='Fraction',
                                                        field_names=['training', 'validating', 'testing'])):

        # get the collection of modelling parameters
        configurations = config.Config()
        self.modelling = configurations.modelling()

        # initialise a splitting object
        self.splitting = src.modelling.DataSplitting.DataSplitting(fraction=fraction)

        # get the list of the data files that would be used for modelling
        self.source = os.path.join(os.getcwd(), 'warehouse', 'design', 'raw')
        self.files = glob.glob(pathname=os.path.join(self.source, '*.csv'))

        # storage
        self.storage = os.path.join(os.getcwd(), 'warehouse', 'modelling', 'splitting')
        self.__path()

    def __path(self):
        """

        :return:
        """

        if not os.path.exists(self.storage):
            os.makedirs(self.storage)

    @dask.delayed
    def __read(self, stem):
        """

        :return:
        """

        try:
            data = pd.read_csv(filepath_or_buffer=os.path.join(self.source, '{}.csv'.format(stem)),
                               usecols=self.modelling.variables, header=0, encoding='utf-8')
        except RuntimeError as err:
            raise Exception(err)

        return data

    @dask.delayed
    def __split(self, blob):
        """

        :return:
        """

        return self.splitting.exc(data=blob)

    @dask.delayed
    def __indexing(self, index: int, blob: pd.DataFrame):
        """

        :return:
        """

        group = pd.DataFrame(data={'group': np.repeat(index, blob.shape[0], axis=0)})

        return pd.concat((group, blob), axis=1)

    @staticmethod
    def __structures(frames):

        training = pd.concat([frame[0] for frame in frames], axis=0, ignore_index=True)
        validating = pd.concat([frame[1] for frame in frames], axis=0, ignore_index=True)
        testing = pd.concat([frame[2] for frame in frames], axis=0, ignore_index=True)

        return training, validating, testing

    def exc(self):

        files = self.files
        stems = [pathlib.Path(file).stem for file in files]
        indices = np.linspace(start=1, stop=len(files), num=len(files), endpoint=True)
        pd.DataFrame(data={'index': indices, 'stem': stems}) \
            .to_csv(path_or_buf=os.path.join(self.storage, 'indexing.csv'), header=True, index=False, encoding='utf-8')

        computations = []
        for index, stem in zip(indices, stems):
            readings = self.__read(stem=stem)
            indexed = self.__indexing(index=index, blob=readings)
            splits = self.__split(blob=indexed)

            computations.append(splits)

        dask.visualize(computations, filename='splitting', format='pdf')
        frames = dask.compute(computations, scheduler='processes')[0]

        return self.__structures(frames=frames)
