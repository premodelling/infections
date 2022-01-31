import tensorflow as tf


class ModellingBaseline(tf.keras.Model):

    def __init__(self, label_index=None):
        """

        :param label_index:
        """

        super().__init__()
        self.label_index = label_index

    def call(self, inputs):
        """

        :param inputs:
        :return:
        """

        if self.label_index is None:
            return inputs

        result = inputs[:, :, self.label_index]

        return result[:, :, tf.newaxis]
