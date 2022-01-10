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

    agegroupsexmsoa = src.preprocessing.agegroupsexmsoa.AgeGroupSexMSOA().exc()
    logger.info(agegroupsexmsoa)

    exceptions = src.preprocessing.exceptions.Exceptions().exc()
    logger.info(exceptions)

    populationsltla = src.preprocessing.populationsltla.PopulationsLTLA().exc()
    logger.info(populationsltla)

    agegroupsexltla = src.preprocessing.agegroupsexltla.AgeGroupSexLTLA().exc()
    logger.info(agegroupsexltla)


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
    import src.preprocessing.agegroupsexmsoa
    import src.preprocessing.exceptions
    import src.preprocessing.populationsltla
    import src.preprocessing.agegroupsexltla

    main()
