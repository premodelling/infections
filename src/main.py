import logging
import os
import sys


def main():

    logger.info('infections')

    # preprocessing supplementary data files: PHE MSOA/Trust Patients, populations, geographic districts
    preprocessing.interface.main()

    # coronavirus.gov.uk
    virus.interface.main()

    # determining multi-granularity patient flow weights, from LTLA -> NHS Trust, via MSOA -> NHS Trust numbers
    catchments.interface.main()

    # determining the vaccinations specific multi-granularity patient flow weights; different because
    # its age groupings/brackets differ from the standard 5 year groupings/brackets
    vaccinations.interface.main()

    # estimating NHS Trust coronavirus measures per NHS Trust BY transforming LTLA measures to
    # weighted NHS Trust Components via the calculated multi-granularity patient flow weights
    #
    # subsequently, a tensor consisting of the raw matrix of independent variables vectors, and
    # the outcome vector is constructed
    #
    design.interface.main()

    
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
    import preprocessing.interface
    import virus.interface
    import catchments.interface
    import vaccinations.interface
    import design.interface

    main()
