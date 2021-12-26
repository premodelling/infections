import logging
import os
import sys


def main():

    # extract weights by trust
    messages = src.weights.baseline.Baseline().exc()
    logger.info(messages)

    # due to time limitations, instead of predicting future weights, the latest weights will be used
    messages = src.weights.focus.Focus(year=2019).exc()
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
    import src.weights.baseline
    import src.weights.focus

    main()
