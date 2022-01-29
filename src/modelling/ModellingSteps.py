import tensorflow as tf


class ModellingSteps:

    def __init__(self):
        """

        """

        self.epochs = 100

    def modelling(self, model, window, patience=13):

        # noinspection PyUnresolvedReferences
        early_stopping = tf.keras.callbacks.EarlyStopping(monitor='val_loss',
                                                          patience=patience,
                                                          mode='min')

        model.compile(loss=tf.losses.MeanSquaredError(),
                      optimizer=tf.optimizers.Adam(),
                      metrics=[tf.metrics.MeanAbsoluteError()])

        history = model.fit(window.train, epochs=self.epochs,
                            validation_data=window.validate,
                            callbacks=[early_stopping])
        return history
