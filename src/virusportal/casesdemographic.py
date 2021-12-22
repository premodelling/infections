import collections
import os

import dask
import pandas as pd

import src.virusportal.nestedfield


class Demographics:

    def __init__(self, field, path: str):
        """

        :param field: the nested demographic field
        :param path:
        """

        self._field = field

        # initialise the nested field reading function
        self.nested = src.virusportal.nestedfield.NestedField(field=self._field)

        # the age groups
        self._age_group = ['00_04', '05_09', '10_14', '15_19', '20_24', '25_29', '30_34', '35_39',
                           '40_44', '45_49', '50_54', '55_59', '60_64', '65_69', '70_74', '75_79',
                           '80_84', '85_89', '90+', 'unassigned']

        self.rename = {'00_04': '0-4', '05_09': '5-9', '10_14': '10-14', '15_19': '15-19', '20_24': '20-24',
                       '25_29': '25-29', '30_34': '30-34', '35_39': '35-39', '40_44': '40-44',
                       '45_49': '45-49', '50_54': '50-54', '55_59': '55-59', '60_64': '60-64', '65_69': '65-69',
                       '70_74': '70-74', '75_79': '75-79', '80_84': '80-84', '85_89': '85-89'}

        # storage
        self.storage = os.path.join(os.getcwd(), 'warehouse', 'virus', path)
        self.__path()

    def __path(self):
        """

        :return:
        """

        if not os.path.exists(self.storage):
            os.makedirs(self.storage)

    @dask.delayed
    def __read(self, parameters):
        """

        :return:
        """

        # get the JSON data set
        return self.nested.exc(parameters=parameters)

    @dask.delayed
    def __structure(self, blob):

        if blob is not None:
            # read it into a data frame, select the correct range of age group elements, pivot
            supplement: pd.DataFrame = pd.json_normalize(data=blob['data'], record_path=self._field, meta=['date'])
            supplement = supplement.loc[supplement.age.isin(self._age_group), :]
            frame = supplement.pivot(index='date', columns='age', values='cases')
        else:
            frame = pd.DataFrame()

        frame.rename(columns=self.rename, inplace=True)

        return frame

    @dask.delayed
    def __write(self, frame: pd.DataFrame, parameters: collections.namedtuple) -> str:
        """

        :param frame:
        :param parameters:
        :return:
        """

        try:
            if not frame.empty:
                frame.to_csv(path_or_buf=os.path.join(self.storage, '{}.csv'.format(parameters.area_code)),
                             index=True, header=True, encoding='utf-8')
                return '{}: succeeded'.format(parameters.area_code)
            else:
                return '{}: no data'.format(parameters.area_code)

        except RuntimeError as err:
            raise Exception(err)

    def exc(self, parameters_: list):

        computations = []
        for parameters in parameters_:

            blob = self.__read(parameters=parameters)
            frame = self.__structure(blob=blob)
            message = self.__write(frame=frame, parameters=parameters)
            computations.append(message)

        dask.visualize(computations, filename='demographics', format='pdf')
        messages = dask.compute(computations, scheduler='processes')[0]

        return messages
