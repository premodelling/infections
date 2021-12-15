"""
Module patients:
    Splits the NHS Trust catchment populations per Middle Super Output Area into yearly files
"""
import os
import pandas as pd
import dask


class Patients:

    def __init__(self):
        """
        Constructor

        """

        self.uri = 'data/catchment/2020 Trust Catchment Populations_Supplementary MSOA Analysis.xlsx'
        self.sheet_name = 'All Admissions'
        self.usecols = ['CatchmentYear', 'msoa', 'TrustCode', 'patients', 'total_patients']

        self.storage = os.path.join(os.getcwd(), 'warehouse', 'admissions')
        self.__path()

        self.patients = self.__read()

    def __path(self):
        """
        Ascertains the existence of warehouse/admissions/

        :return:
        """

        if not os.path.exists(self.storage):
            os.makedirs(self.storage)

    def __read(self) -> pd.DataFrame:
        """
        Reads the patients per Middle Super Output Area (MSOA) data from the
        large Excel file

        :return:
        """

        try:
            patients = pd.read_excel(io=self.uri, sheet_name=self.sheet_name, header=0, usecols=self.usecols)
        except RuntimeError as err:
            raise Exception(err)

        return patients

    @dask.delayed
    def __select(self, year) -> pd.DataFrame:
        """
        Selects the year of interest

        :param year:
        :return:
        """
        
        return self.patients.copy()[self.patients['CatchmentYear'] == year, :]
        
    @dask.delayed
    def __write(self, frame: pd.DataFrame, year: int) -> str:
        """
        Save each year's admissions data to a warehouse directory

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

        years = self.patients['CatchmentYear'].unique()

        computations = []
        for year in years:
            frame = self.__select(year=year)
            message = self.__write(frame=frame)
            computations.append(message)

        dask.visualize(computations, filename='patients', format='pdf')
        details = dask.compute(computations, scheduler='processes')[0]

        return details
