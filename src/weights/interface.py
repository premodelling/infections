import logging
import os
import sys


def main():

    # extract weights by trust
    messages = src.weights.weightsltla.WeightsLTLA().exc()
    logger.info(messages)


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
    import src.weights.weightsltla

    main()
