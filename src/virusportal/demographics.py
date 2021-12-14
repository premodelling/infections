import pandas as pd

import src.virusportal.nestedfield


class Demographics:

    def __init__(self, field):
        """

        :param field: the nested demographic field
        """

        self._field = field

        # initialise the nested field reading function
        self.nested = src.virusportal.nestedfield.NestedField(field=self._field)

        # the age groups
        self._age_group = ['00_04', '05_09', '10_14', '15_19', '20_24', '25_29', '30_34', '35_39',
                           '40_44', '45_49', '50_54', '55_59', '60_64', '65_69', '70_74', '75_79',
                           '80_84', '85_89', '90+', 'unassigned']

    def exc(self, area_code):

        # get the JSON data set
        blob = self.nested.exc(area_code=area_code)

        # read it into a data frame
        supplement:pd.DataFrame = pd.json_normalize(data=blob['data'], record_path=self._field, meta=['date'])

        # select the correct range of age group elements
        supplement = supplement.loc[supplement.age.isin(self._age_group), :]

        return supplement.pivot(index='date', columns='age', values='cases')
