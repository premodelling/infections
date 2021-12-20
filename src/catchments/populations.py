import pandas as pd
import os.path


class Populations:

    def __init__(self, source_path):
        """

        :param source_path:
        """

        self.source_path = source_path

    def __agg_msoa(self):
        """

        :return:
        """

    def __agg_ltla(self):
        """

        :return:
        """

    def __agg_merge(self):
        """

        :return:
        """

    def __read(self, filename: str) -> pd.DataFrame:

        try:
            frame = pd.read_csv(filepath_or_buffer=os.path.join(self.source_path, filename), header=0, encoding='utf-8')
        except RuntimeError as err:
            raise Exception(err)

        return frame

    def exc(self, filename: str):
        """

        :param filename:
        :return:
        """