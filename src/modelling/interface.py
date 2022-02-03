import collections
import logging
import os
import sys


def main():

    logger.info('modelling')

    # Foremost: The data sets for training, validating, and testing
    training, validating, testing = src.modelling.DataStreams.DataStreams(root=root, fraction=Fraction._make(
        (0.75, 0.15, 0.10))).exc()

    # Reconstructions: Each data set is a concatenation of records from various NHS Trusts, however because
    # the aim is a single predicting/forecasting model for all trusts, the data should be reconstructed ...
    reconstructions = src.modelling.DataReconstructions.DataReconstructions()
    training = reconstructions.exc(blob=training)
    validating = reconstructions.exc(blob=validating)
    testing = reconstructions.exc(blob=testing)

    # Using difference values rather than actual values
    differences = src.modelling.Differences.Differences()
    training = differences.exc(blob=training)
    validating = differences.exc(blob=validating)
    testing = differences.exc(blob=testing)

    # normalisation
    normalisation = src.modelling.DataNormalisation.DataNormalisation(reference=training)
    training_ = normalisation.normalise(blob=training)
    validating_ = normalisation.normalise(blob=validating)
    testing_ = normalisation.normalise(blob=testing)

    training_.drop(columns='point', inplace=True)
    validating_.drop(columns='point', inplace=True)
    testing_.drop(columns='point', inplace=True)

    # modelling
    arguments = Arguments(input_width=None, label_width=output_steps, shift=output_steps,
                          training_=training_, validating_=validating_, testing_=testing_,
                          label_columns=['estimatedNewAdmissions'])

    validations, tests = src.modelling.Estimates.Estimates(n_features=training_.shape[1],
                                                           output_steps=output_steps).exc(widths=widths,
                                                                                          arguments=arguments)

    logger.info(validations)
    logger.info(tests)


if __name__ == '__main__':
    root = os.getcwd()
    sys.path.append(root)
    sys.path.append(os.path.join(root, 'src'))

    # Logging
    logging.basicConfig(level=logging.INFO,
                        format='\n\n%(message)s\n%(asctime)s.%(msecs)03d',
                        datefmt='%Y-%m-%d %H:%M:%S')
    logger = logging.getLogger(__name__)

    # libraries
    import src.modelling.DataStreams
    import src.modelling.DataReconstructions
    import src.modelling.Differences
    import src.modelling.DataNormalisation
    import src.modelling.Estimates

    # setting-up
    Fraction = collections.namedtuple(
        typename='Fraction',
        field_names=['training', 'validating', 'testing'])

    Arguments = collections.namedtuple(
        typename='Arguments',
        field_names=['input_width', 'label_width', 'shift', 'training_', 'validating_', 'testing_', 'label_columns'])

    widths = range(18, 40)
    output_steps = 15

    main()
