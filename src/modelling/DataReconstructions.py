import pandas as pd


class DataReconstructions:

    def __init__(self):
        """

        """

        # the index point
        self.point = 'point'

    def __rearrange(self, blob):

        # the fields
        fields = [self.point] + blob.columns.to_list()

        # add a index points column
        blob.loc[:, self.point] = blob.index.values

        # ensure that the frame is arranged by point then group
        rearranged = blob.sort_values(by=[self.point, 'group'])
        rearranged = rearranged[fields]
        rearranged.drop(columns=['date'], inplace=True)

        # re-index
        rearranged.reset_index(drop=True, inplace=True)

        return rearranged

    def exc(self, blob: pd.DataFrame) -> pd.DataFrame:
        """

        :return:
        """

        return self.__rearrange(blob=blob)
