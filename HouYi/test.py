from harness.demo_translator_harness import TranslatorHarness
from example_apps.write_sonic import WriteSonicHarness
from example_apps.finance_assistant import FinanceAssistantHarness
from example_apps.travel_planner import TravelPlannerHarness
from example_apps.english_trainer import EnglishTrainerHarness
from harness.analyze_harness import AnalyzeHarness
from intention.write_code import WriteCode
from intention.spam_generation import SpamGeneration
from intention.prompt_leakage import PromptLeakage
from intention.information_gathering import InformationGathering
from intention.content_manipulation import ContentManipulation

from demo import inject

import loguru
import multiprocessing
import os

if not os.path.exists('logs'):
    os.makedirs('logs')

def run_inject(intention, application_harness, log_file, status_dict):
    # Configure logger for each subprocess
    logger = loguru.logger
    logger.add(log_file, rotation="1 MB", retention="10 days")
    
    for i,harness in enumerate(application_harness):
        logger.info(f"--------Starting injection({i+1}/{len(application_harness)}) for {intention.__class__.__name__} on {harness.__class__.__name__}")
        inject(intention, harness, all_combinations=None,json_dir='result')
        logger.info(f"--------Finished injection({i+1}/{len(application_harness)}) for {intention.__class__.__name__} on {harness.__class__.__name__}")
    
    #
    status_dict[intention.__class__.__name__] = True
 
 
 
if __name__ == "__main__":
    
    intentions = [
        WriteCode(),
        SpamGeneration(),
        PromptLeakage(),
        InformationGathering(),
        ContentManipulation()
    ]
    
    harnesses = [
        AnalyzeHarness(),
        WriteSonicHarness(),
        FinanceAssistantHarness(),
        TravelPlannerHarness(),
        EnglishTrainerHarness()
    ]
    

    processes = []
    manager = multiprocessing.Manager()
    status_dict = manager.dict()

    for intention in intentions:
        status_dict[intention.__class__.__name__] = False
        log_file = f"logs/{intention.__class__.__name__}.log"
        p = multiprocessing.Process(target=run_inject, args=(intention, harnesses, log_file, status_dict))
        p.start()
        processes.append(p)

    import time
    while not all(status_dict.values()):
        time.sleep(1) 

    for p in processes:
        p.join()


    print("///// All injections completed.")
