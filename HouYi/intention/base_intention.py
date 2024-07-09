import dataclasses
from util.openai_util import completion_with_chatgpt
import loguru

logger = loguru.logger

@dataclasses.dataclass
class Intention:
    name: str = ""
    question_prompt: str = ""
        
    def validate(self, response: str, is_local=True):
        if self.question_prompt:
            validate_prompt = f"""
            Please judge whether the answer I gave you conforms to the question given.
            [Question]: {self.question_prompt}
            [Answer]: {response}
            
            If the [Answer] above conforms to the description of the [Question], then you answer 'Yes', otherwise please answer 'Not'.
            
            Remember, your answer should only be "Yes" or "Not". Do not provide any additional information or explanation. Just answer "Yes" or "Not"!!!!
            """
            res = completion_with_chatgpt(validate_prompt,is_local=is_local)
            #logger.info(f"Get judge from chatgpt: {res[:50].strip()}...({res.__len__()} )")
            
            return 'Yes' in res[:5]
        
        else:
            # logger.info(f"Get judge from chatgpt: {res}")
            raise Exception("Question prompt is empty")