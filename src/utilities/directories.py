"""
Module directories
"""
import os


class Directories:
    """
    Class Directories: Preparing directories
    """

    def __init__(self):
        """
        The constructor

        """

    @staticmethod
    def delete(text: str):
        """

        :param text: path & file string
        :return:
        """

        # Foremost, delete files

        files_ = [os.remove(os.path.join(base, file))
                  for base, _, files in os.walk(text) for file in files]

        if any(files_):
            raise Exception('Unable to delete all files within path {}'.format(text))

        # ... then, directories

        directories_ = [os.removedirs(os.path.join(base, directory))
                        for base, directories, _ in os.walk(text, topdown=False) for directory in directories
                        if os.path.exists(os.path.join(base, directory))]

        if any(directories_):
            raise Exception('Unable to delete all directories within path {}'.format(text))

    @staticmethod
    def create(text: str):
        """

        :param text: path & file string
        :return:
        """

        if not os.path.exists(text):
            os.makedirs(text)

    def exc(self, text):
        """

        :param text: path & file string
        :return:
        """

        self.delete(text=text)
        self.create(text=text)
