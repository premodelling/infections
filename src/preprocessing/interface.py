import logging
import os
import sys


def main():
    # patients = src.preprocessing.patients.Patients().exc()
    # logger.info(patients)

    # populations = src.preprocessing.populations.Populations().exc()
    # logger.info(populations)

    # agegroups = src.preprocessing.agegroups.AgeGroups().exc()
    # logger.info(agegroups)

    # exceptions = src.preprocessing.exceptions.Exceptions().exc()
    # logger.info(exceptions)

    districts = src.preprocessing.districts.Districts().exc()
    logger.info(districts)


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
    import src.preprocessing.exceptions
    import src.preprocessing.districts

    main()
