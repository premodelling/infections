"""
Creates concatenated forms of the raw design matrices of warehouse/design/raw/.  The records per trust are
differentiable via a new field labelled 'trust_code'

"""
import glob
import os
import pathlib

import dask
import pandas as pd

import config


class Temporary:

    def __init__(self):

        # expected age groups
        age_groups = config.Config().age_groups
        self.age_groups = ['EDC{}'.format(age_group) for age_group in age_groups]

        # source
        self.source_path = os.path.join('warehouse', 'design', 'raw')

        # storage
        self.storage = os.path.join('graphics', 'data')
        if not os.path.exists(self.storage):
            os.makedirs(self.storage)

    @dask.delayed
    def __read(self, uri):

        try:
            frame = pd.read_csv(filepath_or_buffer=uri, header=0, encoding='utf-8')
        except RuntimeError as err:
            raise Exception(err)

        frame.loc[:, 'trust_code'] = pathlib.Path(uri).stem

        return frame

    def __split(self, frame: pd.DataFrame):

        dgr = frame[['date', 'trust_code'] + self.age_groups]
        dgr = dgr.melt(id_vars=['date', 'trust_code'], var_name='age_group', value_name='daily_cases')
        agg = frame.drop(columns=self.age_groups)

        return dgr, agg

    def __write(self, frame: pd.DataFrame, filename: str):

        path = os.path.join(self.storage, filename)

        try:
            frame.to_csv(path_or_buf=path, index=False, header=True, encoding='utf-8')
            return 'a concatenated form of the raw design matrices has been created: {}'.format(path)
        except RuntimeError as err:
            raise Exception(err)

    def exc(self):

        files = glob.glob(os.path.join(self.source_path, '*.csv'))

        computations = []
        for file in files:
            frame = self.__read(uri=file)
            computations.append(frame)

        dask.visualize(computations, filename='temporary', format='pdf')
        calculations = dask.compute(computations, scheduler='processes')[0]

        # concatenating the data frames of the list
        raw = pd.concat(calculations, axis=0, ignore_index=True)

        # split for graph drawing
        disaggregated, aggregated = self.__split(frame=raw)

        # save
        messages = [self.__write(frame=disaggregated, filename='disaggregated.csv'),
                    self.__write(frame=aggregated, filename='aggregated.csv'),
                    self.__write(frame=raw, filename='raw.csv')]

        return messages
