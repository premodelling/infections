import os.path

import pandas as pd


class Patients:

    def __init__(self, source_path):
        """

        """

        self.source_path = source_path

    def read(self, filename) -> pd.DataFrame:

        try:
            frame = pd.read_csv(filepath_or_buffer=os.path.join(self.source_path, filename), header=0, encoding='utf-8')
        except RuntimeError as err:
            raise Exception(err)

        return frame
