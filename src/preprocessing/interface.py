import logging
import os
import sys


def main():

    logger.info('preprocessing ...')

    districts = src.preprocessing.districts.Districts().exc()
    logger.info(districts)

    patients = src.preprocessing.patients.Patients().exc()
    logger.info(patients)

    populations_msoa = src.preprocessing.populationsmsoa.PopulationsMSOA().exc()
    logger.info(populations_msoa)

    age_group_sex_msoa = src.preprocessing.agegroupsexmsoa.AgeGroupSexMSOA().exc()
    logger.info(age_group_sex_msoa)

    exceptions = src.preprocessing.exceptions.Exceptions().exc()
    logger.info(exceptions)

    populations_ltla = src.preprocessing.populationsltla.PopulationsLTLA().exc()
    logger.info(populations_ltla)

    age_group_sex_ltla = src.preprocessing.agegroupsexltla.AgeGroupSexLTLA().exc()
    logger.info(age_group_sex_ltla)

    vaccinations_msoa = src.preprocessing.vaccinationgroupsmsoa.VaccinationGroupsMSOA().exc()
    logger.info(vaccinations_msoa)

    vaccinations_ltla = src.preprocessing.vaccinationgroupsltla.VaccinationGroupsLTLA().exc()
    logger.info(vaccinations_ltla)


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

    import src.preprocessing.vaccinationgroupsmsoa
    import src.preprocessing.vaccinationgroupsltla

    main()
