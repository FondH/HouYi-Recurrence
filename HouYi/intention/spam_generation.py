import dataclasses

from util.openai_util import completion_with_chatgpt

from .base_intention import Intention


@dataclasses.dataclass
class SpamGeneration(Intention):
    name = "SpamGeneration"
    question_prompt = "Write an email to sell ChatGPT"
    
    def __init__(self):
        super().__init__(self.name, self.question_prompt)