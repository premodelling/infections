import matplotlib.pyplot as plt

import src.prototyping.WindowGenerator


class WindowGraphs:

    def __init__(self, input_width, label_width, shift,
                 training, validating, testing, label_columns):
        """
        
        :param input_width:
        :param label_width:
        :param shift:
        :param training:
        :param validating:
        :param testing:
        :param label_columns:
        """

        self.window = src.prototyping.WindowGenerator.WindowGenerator(
            input_width=input_width, label_width=label_width, shift=shift,
            training=training, validating=validating, testing=testing,
            label_columns=label_columns)

    def plot(self, model=None, column='estimatedNewAdmissions', maximum_subplots=3):
        """
        https://matplotlib.org/stable/gallery/misc/zorder_demo.html

        :param model:
        :param column:
        :param maximum_subplots:
        :return:
        """

        plt.figure(figsize=(11, 8))

        inputs, labels = self.window.example
        column_index = self.window.column_indices[column]
        limits = min(maximum_subplots, len(inputs))

        for n in range(limits):

            plt.subplot(limits, 1, n + 1)
            plt.ylabel(f'{column}\n[normalised]')
            
            # input
            plt.plot(self.window.input_indices, inputs[n, :, column_index],
                     label='Inputs', marker='.', zorder=-10)

            # labels
            if self.window.label_columns:
                label_column_index = self.window.label_columns_indices.get(column, None)
            else:
                label_column_index = column_index
        
            if label_column_index is None:
                continue

            plt.scatter(self.window.label_indices, labels[n, :, label_column_index],
                        edgecolors='k', label='Labels', c='#2ca02c', s=64)

            # predictions
            if model is not None:
                predictions = model(inputs)
                plt.scatter(self.window.label_indices, predictions[n, :, label_column_index],
                            marker='X', edgecolors='k', label='Predictions', c='#ff7f0e', s=64)

            # legend
            if n == 0:
                plt.legend()
