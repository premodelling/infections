import logging
import os
import sys

import collections


def main():

    logger.info('infections')

    # the training, validating, and testing data sets
    Fraction = collections.namedtuple(typename='Fraction', field_names=['training', 'validating', 'testing'])
    training, validating, testing = src.modelling.DataStreams.DataStreams(
        root=root, fraction=Fraction._make((0.75, 0.15, 0.10))).exc()

    logger.info('training data %s', training.shape)
    logger.info('validating data %s', validating.shape)
    logger.info('testing data %s', testing.shape)


if __name__ == '__main__':
    root = os.getcwd()
    sys.path.append(root)
    sys.path.append(os.path.join(root, 'src'))
    sys.path.append(os.path.join(root, 'src', 'preprocessing'))

    # Logging
    logging.basicConfig(level=logging.INFO,
                        format='\n\n%(message)s\n%(asctime)s.%(msecs)03d',
                        datefmt='%Y-%m-%d %H:%M:%S')
    logger = logging.getLogger(__name__)

    # libraries
    import src.modelling.DataStreams

    main()
