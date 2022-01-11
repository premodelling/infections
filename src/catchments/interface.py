import glob
import logging
import os
import pathlib
import sys


def main():

    # Dask is used for LTLA steps.
    for year in years:
        logger.info(year)

        patients = src.catchments.patients.Patients(source_path=path_patients) \
            .read(filename='{}.csv'.format(year))

        populations = src.catchments.populations.Populations(source_path=path_populations) \
            .exc(filename='{}.csv'.format(year))

        aggregates_ltla = src.catchments.aggregatesltla.AggregatesLTLA(patients=patients, populations=populations) \
            .exc()
        ltla = src.catchments.ltla.LTLA(reference=aggregates_ltla, year=year).exc()
        logger.info(ltla)

    messages = src.catchments.weightseriesltla.WeightSeriesLTLA().exc()
    logger.info(messages)


if __name__ == '__main__':

    # paths
    root = os.getcwd()
    sys.path.append(root)
    sys.path.append(os.path.join(root, 'src'))

    # data sources paths
    path_patients = os.path.join(root, 'warehouse', 'patients')
    path_populations = os.path.join(root, 'warehouse', 'populations', 'msoa', 'group')

    # logging
    logging.basicConfig(level=logging.INFO,
                        format='\n\n%(message)s\n%(asctime)s.%(msecs)03d',
                        datefmt='%Y-%m-%d %H:%M:%S')
    logger = logging.getLogger(__name__)

    # libraries
    import src.catchments.weightseriesltla
    import src.catchments.patients
    import src.catchments.populations
    import src.catchments.aggregatesltla
    import src.catchments.ltla

    # years
    years = [int(pathlib.Path(filepath).stem)
             for filepath in glob.glob(os.path.join(path_patients, '*.csv'))]

    main()
