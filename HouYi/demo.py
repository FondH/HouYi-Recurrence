import json
import pathlib

import loguru
import openai

from constant.prompt_injection import PromptInjection
from context_infer import ContextInfer
from harness.base_harness import Harness
from harness.demo_translator_harness import TranslatorHarness
from intention.base_intention import Intention
from intention.write_code import WriteCode
from strategy.disruptor_generation import DISRUPTOR_GENERATOR_LIST
from strategy.framework_generation import FRAMEWORK_GENERATION_STRATEGY
from strategy.separator_generation import SEPARATOR_GENERATOR_LIST
import os
import datetime
logger = loguru.logger

# load config file from root path
# config_file_path = pathlib.Path("./config.json")
# config = json.load(open(config_file_path))
# openai.api_key = config["openai_key"]

# try times
try_times =3


def json_dump(intent_name, data, dir='result'):
    try:
        if os.path.exists(dir) == False:
            os.mkdir(dir,)
        
        today = datetime.datetime.now().strftime("%m%d")
        filename = f"{intent_name}_{today}.json"
        
        counter = 1
        while os.path.exists(os.path.join(dir, filename)):
            filename = f"{intent_name}_{today}_{counter}.json"
            counter += 1

        with open(os.path.join(dir, filename), 'w') as f:
            json.dump(data, f, indent=4)
    
    except Exception as e:
        
        logger.error(f"[json_dump] meet some error: {e}")
        
        
import itertools
_all_combinations = list(itertools.product(FRAMEWORK_GENERATION_STRATEGY, SEPARATOR_GENERATOR_LIST, DISRUPTOR_GENERATOR_LIST))


def inject(intention: Intention, application_harness: Harness, all_combinations=_all_combinations,**kw):
    
    if all_combinations == None:
        all_combinations = _all_combinations
        
    is_local = kw['is_local'] if 'is_local' in kw.keys() else False

    
    st_time = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    records = {}
    success = []
    fails =  []
    is_succeed = False
    # infer context
    context_infer = ContextInfer(application_harness)
    # generate framework
    for indx, (framework_strategy_class, 
                      separator_generator_class, 
                      disruptor_generator_class) in enumerate(all_combinations):
        # generate separator
        framework_generation_strategy = framework_strategy_class()
        framework = framework_generation_strategy.generate_framework(application_harness.application_document,is_local=is_local)
        # generate separator
        separator_generator = separator_generator_class()
        separator = separator_generator.generate_separator()
        # generate disruptor
        disruptor_generator = disruptor_generator_class()
        disruptor = disruptor_generator.generate_disruptor()

        prompt_injection = PromptInjection(intention=intention)
        prompt_injection.prompt = f"{framework}"\
                                  f"{separator}"\
                                  f"{prompt_injection.intention.question_prompt}"\
                                  f"{disruptor}"

        type = f"{framework_generation_strategy.generator_name}_{separator_generator.generator_name}_{disruptor_generator.generator_name}"
        records[type] = []

        for i in range(try_times):

            response = application_harness.run_harness(prompt_injection,is_local=is_local)
            # logger.warning(f"\n---- Test current strategy with target App\n"
            #             f"Strategy: {type} try times: {i + 1}/{try_times} \n"
            #             f"inject prompt: {prompt_injection.prompt[:60].strip()} ..({len(prompt_injection.prompt)})\n"
            #             f"response: {response[:60].strip()}..({len(response)})"
            #             )
        
            # check if the response is successful
            if intention.validate(response, is_local=is_local):
                success.append(f'{type}--{i + 1}/{try_times}')
                logger.info(f"Progress: {indx + 1}/{len(all_combinations)} [{i + 1}/{try_times}] <Yes> Strategy: {type}, ")
                #logger.success(f"Judge result: Yes")
                records[type].append({
                    'status': 'success',
                    'response': response,
                    'inject_prompt': prompt_injection.prompt,
                    'strategy': type,
                    'Myintent': intention.question_prompt,
                })

                break
            else:
                records[type].append({
                    'status': 'failed',
                    'response': response,
                    'inject_prompt': prompt_injection.prompt,
                    'strategy': type,
                    'Myintent': intention.question_prompt,
                })
                fails.append(f'{type}--{i + 1}/{try_times}')
                logger.info(f"Progress: {indx + 1}/{len(all_combinations)} [{i + 1}/{try_times}] <No> Strategy {type}, ")
                #logger.error(f"Judge result: No")
                
            # infer context
            # question = context_infer.infer(
            #     prompt_injection.intention.question_prompt, response
            # )
            # logger.info(f"Context Infer Question: {question}")
            refined_prompt = context_infer.generate_refine_prompt(framework,
                                                                  separator, disruptor, 
                                                                  intention.question_prompt, 
                                                                  is_local=is_local)
            #logger.info(f"Has refined the inject prompt")
            prompt_injection.prompt = refined_prompt

                    
    ed_time = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
     
    json_name = kw['json_name'] if 'json_name' in kw.keys() else None
    json_dir = kw['json_dir'] if 'json_dir' in kw.keys() else None
    if not json_name:
        json_name = f'{application_harness.name}~{intention.name}'
    json_dump(json_name, {'succeed':success, 
                        'st_time':st_time,
                        'et_time':ed_time,
                        'fails':fails,
                        'success_rate':len(success)/len(fails)+len(success),
                        'intention':intention.question_prompt ,
                        'details':records}, dir=json_dir)
    return is_succeed, success


def ablatate(intention: Intention, application_harness: Harness, is_local=False, json_dir='./result/Ablation'):

    from strategy.framework_generation import FRAMEWORK_GENERATION_STRATEGY
    from strategy.separator_generation import SyntaxSeparatorGenerator,  LanguageSeparatorGenerator
    from strategy.separator_generation import ReasoningSemanticSeparatorGenerator,  IgnoringSemanticSeparatorGenerator,AdditionalSemanticSeparatorGenerator
    from strategy.disruptor_generation import PlainDisruptorGenerator
    
    only_SyntaxSeparatorGenerator_iterater = list(itertools.product(FRAMEWORK_GENERATION_STRATEGY,[SyntaxSeparatorGenerator],[PlainDisruptorGenerator]))
    only_LanguageSeparatorGenerator_iterater = list(itertools.product(FRAMEWORK_GENERATION_STRATEGY,[LanguageSeparatorGenerator],[PlainDisruptorGenerator]))
    only_SemanticSeparatorGenerator_iterater = list(itertools.product(FRAMEWORK_GENERATION_STRATEGY,[
                ReasoningSemanticSeparatorGenerator, 
                IgnoringSemanticSeparatorGenerator, 
                AdditionalSemanticSeparatorGenerator],[PlainDisruptorGenerator]))
    
    logger.info(f"***Begin only_SyntaxSeparator 1/3 study on {application_harness.name} with {intention.name}")
    
    inject(intention, application_harness, only_SyntaxSeparatorGenerator_iterater,   is_local=is_local, 
           json_name=f"{application_harness.name}only_SyntaxSeparator",json_dir=json_dir)
    
    logger.info(f"***Begin only_LanguageSeparator 2/3 study on {application_harness.name} with {intention.name}")
    
    inject(intention, application_harness, only_LanguageSeparatorGenerator_iterater, is_local=is_local,
           json_name=f"{application_harness.name}_only_LanguageSeparator",json_dir=json_dir)
    
    logger.info(f"***Begin only_SemanticSeparator 3/3 study on {application_harness.name} with {intention.name}")
    
    inject(intention, application_harness, only_SemanticSeparatorGenerator_iterater, is_local=is_local,
           json_name=f"{application_harness.name}_only_SemanticSeparator",json_dir=json_dir)
    
def main():
    # init prompt injection intention
    write_code_intention = WriteCode()

    # init prompt injection harness
    application_harness = TranslatorHarness()

    # begin injection
    is_success, injected_prompt = inject(write_code_intention, application_harness)

    if is_success:
        logger.info(f"Success! Injected prompt: {injected_prompt}")
    else:
        logger.info(f"Failed! Injected prompt: {injected_prompt}")


if __name__ == "__main__":
    main()
