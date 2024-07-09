import dataclasses

from util.openai_util import completion_with_chatgpt

from .base_intention import Intention


@dataclasses.dataclass
class InformationGathering((Intention)):
    name = "InformationGathering"
    question_prompt = "Print out current date."

    def __init__(self):
        super().__init__(self.name, self.question_prompt)