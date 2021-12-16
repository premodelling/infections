import os
import logging
import pandas as pd
import numpy as np

import config


class Populations:

    def __init__(self):
        """
        Constructor
        """

        self.details, self.ages = config.Config().population()
        self.source = os.path.join(os.getcwd(), 'data', 'populations')

        # storage
        self.storage = os.path.join(os.getcwd(), 'warehouse', 'populations', 'single')
        self.__path()

        # logging
        logging.basicConfig(level=logging.INFO,
                            format='\n\n%(message)s\n%(asctime)s.%(msecs)03d',
                            datefmt='%Y-%m-%d %H-%M-%S')
        self.logger = logging.getLogger(__name__)

    def __path(self):
        """
        Ascertains the existence of warehouse/populations/single

        :return:
        """

        if not os.path.exists(self.storage):
            os.makedirs(self.storage)

    def __read(self, detail) -> pd.DataFrame:
        """
        Reads population files

        :param detail:
        :return:
        """

        readings = []
        for index in np.arange(len(detail.sheets)):

            try:
                frame = pd.read_excel(io=os.path.join(self.source, detail.filename),
                                      sheet_name=detail.sheets[index], header=detail.header,
                                      usecols=detail.cells)
                if detail.overflow is not None:
                    frame = frame.copy().loc[~frame[detail.overflow].notna(), :]
            except RuntimeError as err:
                raise Exception(err)

            frame.rename(columns={detail.keys[0]: 'msoa'}, inplace=True)
            frame = frame.copy().loc[frame['msoa'].str.startswith('E'), :]
            frame = frame.copy()[['msoa'] + self.ages]
            frame.loc[:, 'sex'] = detail.sex[index]

            readings.append(frame)

        return pd.concat(readings, axis=0, ignore_index=True)

    def __write(self, frame: pd.DataFrame, year: int) -> str:
        """

        :param frame:
        :param year:
        :return:
        """

        try:
            frame.to_csv(path_or_buf=os.path.join(self.storage, '{}.csv'.format(year)),
                         index=False, header=True, encoding='utf-8')
            return '{}: succeeded'.format(year)
        except RuntimeError as err:
            raise Exception(err)

    def exc(self):
        """

        :return:
        """

        messages = []
        for detail in self.details:

            estimates = self.__read(detail=detail)
            message = self.__write(frame=estimates, year=detail.year)
            messages.append(message)

        return messages
