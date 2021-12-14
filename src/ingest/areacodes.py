import pandas as pd


class AreaCodes:

    def __init__(self):
        """

        """

    def __lad(self):
        """
        Find an official dicionary that includes 'msoa11cd', 'ladcd', and 'country'.  Hence, we'll
        be able to select England only LADCD/LTLA codes.

        :return:
        """

        try:
            lad = pd.read_csv(filepath_or_buffer='data/catchment/LSOA_MSOA_LAD_MAY20_UK_LU.csv',
                              header=0, usecols=['msoa11cd', 'ladcd'], encoding='utf-8')
        except RuntimeError as err:
            raise Exception(err)

        lad.drop_duplicates(inplace=True, ignore_index=True)

        return lad

    @staticmethod
    def __ltla_england():
        
        try:
            ltla = pd.read_excel(io='data/catchment/2021 Trust Catchment Populations_Supplementary Trust Area lookup.xlsx',
                                 sheet_name='Trust Area Lookup', header=0, usecols=['LTLA21CD'])
        except RuntimeError as err:
            raise Exception(err)

        ltla.drop_duplicates(inplace=True, ignore_index=True)
        
        return ltla
    
    def exc(self):

        lad = self.__lad()
        ltla = self.__ltla_england()

        area_codes = ltla.merge(lad, how='left', left_on='LTLA21CD', right_on='ladcd')
        
        return area_codes
        




