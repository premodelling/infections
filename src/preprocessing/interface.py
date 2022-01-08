import logging
import os
import sys


def main():

    logger.info('preprocessing ...')

    districts = src.preprocessing.districts.Districts().exc()
    logger.info(districts)

    patients = src.preprocessing.patients.Patients().exc()
    logger.info(patients)

    populationsmsoa = src.preprocessing.populationsmsoa.PopulationsMSOA().exc()
    logger.info(populationsmsoa)

    agegroupsmsoa = src.preprocessing.agegroupsmsoa.AgeGroupsMSOA().exc()
    logger.info(agegroupsmsoa)

    exceptions = src.preprocessing.exceptions.Exceptions().exc()
    logger.info(exceptions)

    populationsltla = src.preprocessing.populationsltla.PopulationsLTLA().exc()
    logger.info(populationsltla)

    agegroupsltla = src.preprocessing.agegroupsltla.AgeGroupsLTLA().exc()
    logger.info(agegroupsltla)


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
    import src.preprocessing.districts
    import src.preprocessing.populationsmsoa
    import src.preprocessing.agegroupsmsoa
    import src.preprocessing.exceptions
    import src.preprocessing.populationsltla
    import src.preprocessing.agegroupsltla

    main()
