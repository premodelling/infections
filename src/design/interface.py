import logging
import os
import sys


def main():

    # creating design matrices
    messages = src.design.matrix.Matrix().exc()
    logger.info(messages)

    # concatenated design matrices for graphs
    messages = src.design.temporary.Temporary().exc()
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
    import src.design.matrix
    import src.design.temporary

    main()
