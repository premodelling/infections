import glob
import logging
import os
import pathlib
import sys


def main():

    logger.info('vaccinations')

    # Dask is used for LTLA steps.
    for year in years:

        if year == 2011:
            continue

        logger.info(year)

        patients = src.vaccinations.patients.Patients(source_path=path_patients) \
            .read(filename='{}.csv'.format(year))

        populations = src.vaccinations.populations.Populations(source_path=path_populations) \
            .exc(filename='{}.csv'.format(year))

        aggregates_ltla = src.vaccinations.aggregatesltla.AggregatesLTLA(patients=patients, populations=populations) \
            .exc()
        ltla = src.vaccinations.ltla.LTLA(reference=aggregates_ltla, year=year).exc()
        logger.info(ltla)

    messages = src.vaccinations.weightseriesltla.WeightSeriesLTLA().exc()
    logger.info(messages)


if __name__ == '__main__':

    # paths
    root = os.getcwd()
    sys.path.append(root)
    sys.path.append(os.path.join(root, 'src'))

    # data sources paths
    path_patients = os.path.join(root, 'warehouse', 'patients')
    path_populations = os.path.join(root, 'warehouse', 'vaccinations', 'populations', 'msoa', 'group')

    # logging
    logging.basicConfig(level=logging.INFO,
                        format='\n\n%(message)s\n%(asctime)s.%(msecs)03d',
                        datefmt='%Y-%m-%d %H:%M:%S')
    logger = logging.getLogger(__name__)

    # libraries
    import src.vaccinations.weightseriesltla
    import src.vaccinations.patients
    import src.vaccinations.populations
    import src.vaccinations.aggregatesltla
    import src.vaccinations.ltla

    # years
    years = [int(pathlib.Path(filepath).stem)
             for filepath in glob.glob(os.path.join(path_patients, '*.csv'))]

    main()
