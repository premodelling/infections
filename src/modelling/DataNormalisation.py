
import pandas as pd


class DataNormalisation:

    def __init__(self, reference: pd.DataFrame):
        """

        :param reference:
        """

        self.reference = reference

    def _mean(self):
        """

        :return: the mean of each field
        """

        return self.reference.mean(axis=0)

    def _deviation(self):
        """

        :return: the standard deviation of each field
        """

        return self.reference.std(axis=0)

    def normalise(self, blob: pd.DataFrame) -> pd.DataFrame:
        """

        :param blob:
        :return: a data frame that has been normalised w.r.t. the statistics of the reference frame
        """

        return (blob - self._mean()) / self._deviation()

    def denormalise(self, blob):
        """

        :param blob: a data frame that has been normalised w.r.t. the statistics of the reference frame
        :return: a data frame that has been denormalised w.r.t. the statistics of the reference frame
        """

        return (blob * self._deviation()) + self._mean()

