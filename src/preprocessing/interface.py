import os
import sys
import logging
import glob
import os
import pandas as pd
import numpy as np


def main():

    # patients = src.preprocessing.patients.Patients().exc()
    # logger.info(patients)
    
    # populations = src.preprocessing.populations.Populations().exc()
    # logger.info(populations)

    agegroups = src.preprocessing.agegroups.AgeGroups().exc()
    logger.info(agegroups)
    

if __name__ == '__main__':

    # paths
    root = os.getcwd()
    sys.path.append(root)
    sys.path.append(os.path.join(root, 'src'))

    # logging
    logging.basicConfig(level=logging.INFO,
                        format='\n\n%(message)s\n%(asctime)s.%(msecs)03d',
                        datefmt='%Y-%m-%d %H-%M-%S')
    logger = logging.getLogger(__name__)

    # libraries
    import src.preprocessing.patients
    import src.preprocessing.populations
    import src.preprocessing.agegroups




    main()
