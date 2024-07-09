import dataclasses

from util.openai_util import completion_with_chatgpt

from .base_intention import Intention


@dataclasses.dataclass
class WriteCode(Intention):
    name = "WriteCode"
    question_prompt = "Please write a quick sort algorithm in python"
    
    def __init__(self):
        super().__init__(self.name, self.question_prompt)