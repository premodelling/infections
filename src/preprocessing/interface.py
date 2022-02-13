import logging
import time

import src.preprocessing.patients
import src.preprocessing.districts
import src.preprocessing.populationsmsoa
import src.preprocessing.agegroupsexmsoa
import src.preprocessing.exceptions
import src.preprocessing.populationsltla
import src.preprocessing.agegroupsexltla

import src.preprocessing.vaccinationgroupsmsoa
import src.preprocessing.vaccinationgroupsltla


class Interface:

    def __init__(self):

        # logging
        logging.basicConfig(level=logging.INFO,
                            format='\n\n%(message)s\n%(asctime)s.%(msecs)03d',
                            datefmt='%Y-%m-%d %H-%M-%S')
        self.logger = logging.getLogger(__name__)
        self.logger.info('preprocessing ...')

        # processing times object
        self.times = dict(programs=[])

    @staticmethod
    def __districts() -> dict:

        starting = time.time()
        src.preprocessing.districts.Districts().exc()
        ending = time.time()

        return {'desc': 'districts', 'program': 'preprocessing.districts', 'seconds': ending - starting}

    @staticmethod
    def __patients() -> dict:

        starting = time.time()
        src.preprocessing.patients.Patients().exc()
        ending = time.time()

        return {'desc': 'patients', 'program': 'preprocessing.patients', 'seconds': ending - starting}

    @staticmethod
    def __msoa() -> list:

        starting = time.time()
        src.preprocessing.populationsmsoa.PopulationsMSOA().exc()
        ending = time.time()

        initial = [{'desc': 'MSOA populations',
                    'program': 'preprocessing.populationsmsoa', 'seconds': ending - starting}]

        starting = time.time()
        src.preprocessing.agegroupsexmsoa.AgeGroupSexMSOA().exc()
        ending = time.time()

        initial.append({'desc': 'MSOA populations: age group & sex brackets',
                        'program': 'preprocessing.agegroupsexmsoa', 'seconds': ending - starting})

        return initial

    @staticmethod
    def __ltla() -> list:

        starting = time.time()
        src.preprocessing.populationsltla.PopulationsLTLA().exc()
        ending = time.time()

        initial = [{'desc': 'LTLA populations',
                    'program': 'preprocessing.populationsltla', 'seconds': ending - starting}]

        starting = time.time()
        src.preprocessing.agegroupsexltla.AgeGroupSexLTLA().exc()
        ending = time.time()

        initial.append({'desc': 'LTLA populations: age group & sex brackets',
                        'program': 'preprocessing.agegroupsexltla', 'seconds': ending - starting})

        return initial

    @staticmethod
    def __exceptions() -> dict:

        starting = time.time()
        src.preprocessing.exceptions.Exceptions().exc()
        ending = time.time()

        return {'desc': '2011 demographic data', 'program': 'preprocessing.exceptions', 'seconds': ending - starting}

    @staticmethod
    def __vaccination_brackets() -> list:

        starting = time.time()
        src.preprocessing.vaccinationgroupsmsoa.VaccinationGroupsMSOA().exc()
        ending = time.time()

        initial = [{'desc': 'special MSOA demographics for vac',
                    'program': 'preprocessing.vaccinationgroupsmsoa', 'seconds': ending - starting}]

        starting = time.time()
        src.preprocessing.vaccinationgroupsltla.VaccinationGroupsLTLA().exc()
        ending = time.time()

        initial.append({'desc': 'special LTLA demographics for vac',
                        'program': 'preprocessing.vaccinationgroupsltla', 'seconds': ending - starting})

        return initial

    def exc(self):

        times = self.times

        times['programs'].append(self.__districts())
        times['programs'].append(self.__patients())

        [times['programs'].append(process) for process in self.__msoa()]
        [times['programs'].append(process) for process in self.__ltla()]

        times['programs'].append(self.__exceptions())

        [times['programs'].append(process) for process in self.__vaccination_brackets()]

        return times
