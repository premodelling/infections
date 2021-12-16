import logging
import os
import sys
import requests


def main():
    # patients = src.preprocessing.patients.Patients().exc()
    # logger.info(patients)

    # populations = src.preprocessing.populations.Populations().exc()
    # logger.info(populations)

    # agegroups = src.preprocessing.agegroups.AgeGroups().exc()
    # logger.info(agegroups)

    # exceptions = src.preprocessing.exceptions.Exceptions().exc()
    # logger.info(exceptions)

    url = 'https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/OA11_LSOA11_MSOA11_LAD11_EW_LUv2/' \
          'FeatureServer/0/query?where=1%3D1&outFields=MSOA11CD,MSOA11NM,LAD11CD,LAD11NM&outSR=4326&f=json'

    url = 'https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/MSOA11_WD18_LAD18_EW_LUv2/' \
          'FeatureServer/0/query?where=1%3D1&outFields=MSOA11CD,MSOA11NM,LAD18CD,LAD18NM&outSR=4326&f=json'

    try:
        response = requests.get(url = url)
        response.raise_for_status()
    except requests.RequestException as err:
        raise err.strerror

    extract = response.json()
    logger.info(extract)


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

    main()
