from demo import ablatate, inject

import loguru


json_dir = 'result/Alblation-7'
is_local = False

def run_ablation(intention, application_harness, log_file=None, status_dict=None):
    logger = loguru.logger
    logger.add(log_file, rotation="1 MB", retention="10 days")
    logger.success(f'**** Ablation of [{application_harness.name}] START ****')

    try:
        ablatate(intention, application_harness,is_local=False, json_dir = json_dir)
        
        logger.success(f'----- Ablation of [{application_harness.name}] TWICE ----- ')
        ablatate(intention, application_harness,is_local=False, json_dir = json_dir)
        
        logger.success(f'----- Ablation of [{application_harness.name}] THIRD ----- ')
        ablatate(intention, application_harness,is_local=False, json_dir = json_dir)
        
        logger.success(f'----- Ablation of [{application_harness.name}] THIRD ----- ')
        ablatate(intention, application_harness,is_local=False, json_dir = json_dir)
    except:
        pass

    status_dict[application_harness.__class__.__name__] = True
    logger.success(f'Ablation of [{application_harness.name}] END')

if __name__ == '__main__':
    
    from harness.demo_translator_harness import TranslatorHarness
    from example_apps.write_sonic import WriteSonicHarness
    from example_apps.finance_assistant import FinanceAssistantHarness
    from example_apps.travel_planner import TravelPlannerHarness
    from example_apps.english_trainer import EnglishTrainerHarness
    #application_harness = WriteSonicHarness()
    harnesses = [
        TranslatorHarness(),
        WriteSonicHarness(),
        FinanceAssistantHarness(),
        TravelPlannerHarness(),
        EnglishTrainerHarness()
    ]
    
    # intention
    from intention.prompt_leakage import PromptLeakage
    _intention = PromptLeakage()
    # ablatate(_intention, WriteSonicHarness(),is_local=False, json_dir=json_dir)
    
    # subprocess start
    import multiprocessing

    manager = multiprocessing.Manager()
    status_dict = manager.dict()
    for harness in harnesses:
        status_dict[harness.__class__.__name__] = False
        log_file = f"logs/Ablation/{harness.__class__.__name__}.log"
        p = multiprocessing.Process(target=run_ablation, args=(_intention, harness, log_file, status_dict))
        p.start()


    import time
    while not all(status_dict.values()):
        time.sleep(1) 
    # Application: WriteSonicHarness
    # ablatate(_intention, application_harness,is_local=False)

    

    #inject(_intention, application_harness,is_local=False)