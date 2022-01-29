import pandas as pd


class Differences:

    def __init__(self):
        """

        """

    @staticmethod
    def exc(blob: pd.DataFrame) -> pd.DataFrame:

        difference = blob.drop(columns='point').groupby(by='group', sort=False).diff(periods=1, axis=0)

        frame = blob[['group', 'point']].join(difference, how='left')

        frame.dropna(axis=0, how='any', inplace=True)

        frame.reset_index(drop=True, inplace=True)

        return frame
