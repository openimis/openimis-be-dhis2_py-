# import the logging library
import re



# Create your views here.

from django.core.management.base import BaseCommand
from django.shortcuts import redirect, render
from dhis2_etl.management.utiils import set_logger
from dhis2_etl.scheduled_tasks import adx_monthly_sync

from dhis2_etl.services.claimServices import *
from dhis2_etl.services.fundingServices import *
from dhis2_etl.services.insureeServices import *
from dhis2_etl.services.locationServices import *
from dhis2_etl.services.optionSetServices import *
from dhis2_etl.strategy.adx_client import ADXClient
logger = set_logger()

    


class Command(BaseCommand):
    help = "This command will generate the metadate and data update for dhis2 and push it."

    def add_arguments(self, parser):
        parser.add_argument(
            '--verbose',
            action='store_true',
            dest='verbose',
            help='Be verbose about what it is doing',
        )
        parser.add_argument("start_date", nargs=1, type=lambda s: datetime.datetime.strptime(s, '%Y-%m-%d'))
        parser.add_argument("stop_date", nargs=1, type=lambda s: datetime.datetime.strptime(s, '%Y-%m-%d'))
        parser.add_argument("scope", nargs=1, choices=[
            'all',
            'enroll',
            'insureepolicies',
            'insureepoliciesclaims',
            'createRoot', 
            'orgunit', 
            'optionset',
            'product',
            "gender",
            "profession",
            "education",
            "grouptype",
            "diagnosis",
            "item",
            "service",
            "population",
            "funding",
            ] )


    def handle(self, *args, **options):
        
        verbose = options["verbose"]
        start_date = options["start_date"][0]
        stop_date = options["stop_date"][0]
        scope = options["scope"][0]
        if scope is None:
            scope = "all"
        #if verbose:
        #    logger = set_logger(True)
        logger.info("Start sync Dhis2 %s ", __package__ )
        self.sync_dhis2(start_date, stop_date, scope)
        logger.info("sync Dhis2 done")



    def sync_dhis2(self, start_date, stop_date, scope):
            logger.info("Received task")
            responses = []
            ## TEI and Program enrollment and event
            #########################################
            ## TODO policy only for renewalm insureePolicy for new
            if scope == "all" or scope == "insuree":
                logger.info("start Insuree sync")
                syncInsuree(start_date,stop_date)
            if scope == "all" or scope == "policy":
                logger.info("start Policy sync")
                syncPolicy(start_date,stop_date)
            if scope == "all" or scope == "claim":
                logger.info("start Claim sync")
                syncClaim(start_date,stop_date)
            # OTHER program sync
            ####################
            # manual enrollment to policy program
            if scope == 'enroll':
                logger.info("start Insuree enroll")
                insureeResponse = enrollInsuree(start_date,stop_date)
                #responses.insert(insureeResponse)
            # syncInsuree and Policiy event
            if  scope == "insureepolicies":
                logger.info("start Insuree & policy sync")
                syncInsureePolicy(start_date,stop_date)

            if  scope == "insureepoliciesclaims":
                logger.info("start Insuree & policy & claim sync")
                syncInsureePolicyClaim(start_date,stop_date)
            # ORGUNIT 
            #########
            if scope == 'createRoot':
                sync = createRootOrgUnit()

            if  scope == "orgunit":
                logger.info("start orgUnit sync")
                syncRegion(start_date,stop_date)
                syncDistrict(start_date,stop_date)
                syncWard(start_date,stop_date)
                syncVillage(start_date,stop_date)
                syncHospital(start_date,stop_date)
                syncDispensary(start_date,stop_date)
                syncHealthCenter(start_date,stop_date)
                with ADXClient() as adx_client:
                    adx_client.updateOrgUnitAndCatComboOption()

            # Optionset
            ###########
            if  scope == "optionset" :
                    logger.info("start OptionSets sync")
            if  scope == "optionset" or scope == "product":
                syncProduct(start_date,stop_date)
            if  scope == "optionset" or scope == "gender":
                syncGender(start_date,stop_date)
            if  scope == "optionset" or scope == "profession":
                syncProfession(start_date,stop_date)
            if  scope == "optionset" or scope == "education":
                syncEducation(start_date,stop_date)
            if  scope == "optionset" or scope == "grouptype":
                syncGroupType(start_date,stop_date)
            if  scope == "optionset" or scope == "diagnosis":
                syncDiagnosis(start_date,stop_date)
            if  scope == "optionset" or scope == "item":
                syncItem(start_date,stop_date)
            if  scope == "optionset" or scope == "service":
                syncService(start_date,stop_date)


            # Dataset
            if  scope == "population":
                syncPopulation(start_date)

            # funding
            if  scope == "funding":
                sync_funding(start_date,stop_date)
            logger.info("Finishing task")

            if scope == 'adx-data':
                adx_monthly_sync()


