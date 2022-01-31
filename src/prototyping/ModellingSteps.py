import tensorflow as tf


class ModellingSteps:

    def __init__(self):
        """

        """

        self.epochs = 100

    def modelling(self, model, window, patience=7):
        """

        :param model:
        :param window:
        :param patience:
        :return:
        """

        # noinspection PyUnresolvedReferences
        early_stopping = tf.keras.callbacks.EarlyStopping(monitor='val_loss',
                                                          patience=patience,
                                                          mode='min')

        model.compile(loss=tf.losses.MeanSquaredError(),
                      optimizer=tf.optimizers.Adam(),
                      metrics=[tf.metrics.MeanAbsoluteError()])

        model_ = model.fit(window.train, epochs=self.epochs,
                            validation_data=window.validate,
                            callbacks=[early_stopping])
        return model_
