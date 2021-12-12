import pandas as pd

import src.virusportal.nestedfield


class Demographics:

    def __init__(self, field):
        """

        """

        self._field = field
        self.nested = src.virusportal.nestedfield.NestedField(field=self._field)

    def exc(self, area_code):

        blob = self.nested.exc(area_code=area_code)

        supplement:pd.DataFrame = pd.json_normalize(data=blob['data'], record_path=self._field,
                                                 meta=['date'])

        # ['00_04' '00_59' '05_09' '10_14' '15_19' '20_24' '25_29' '30_34' '35_39'
        #  '40_44' '45_49' '50_54' '55_59' '60+' '60_64' '65_69' '70_74' '75_79'
        #  '80_84' '85_89' '90+' 'unassigned']

        # supplement.pivot(columns='age', values='cases')

        return supplement