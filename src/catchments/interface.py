import os
import sys
import pathlib
import logging
import glob


def main():

    # Do not use dask here.  Instead, use dask for the MSOA & LTLA steps.
    for year in years[:1]:

        logger.info(year)

        patients = src.catchments.patients.Patients(source_path=path_patients)\
            .read(filename='{}.csv'.format(year))
        logger.info(patients)

        populations = src.catchments.populations.Populations(source_path=path_populations)\
            .exc(filename='{}.csv'.format(year))
        logger.info(populations)

        # msoa = src.catchments.msoa.MSOA(year=year).exc(patients=patients, populations=populations)
        # logger.info(msoa)

        aggregates = src.catchments.aggregatesltla.AggregatesLTLA(patients=patients, populations=populations).exc()
        logger.info(aggregates.head())
        logger.info(aggregates.shape)


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
    import src.catchments.patients
    import src.catchments.populations
    import src.catchments.msoa
    import src.catchments.aggregatesltla

    # years
    years = [int(pathlib.Path(filepath).stem)
             for filepath in glob.glob(os.path.join(path_patients, '*.csv'))]

    main()
