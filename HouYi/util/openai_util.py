import openai
from .ollama_util import LocalClient,RemoteClient

def completion_with_openai(text: str, model: str = "gpt-4") -> str:
    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "user", "content": text},
        ],
    )
    return response["choices"][0]["message"]["content"]


# def completion_with_ollama(text: str, model: str = "phi3:mini") -> str:
    
#     my_model_list = ['phi3:mini', 'qwen2:1.5b','qwen2:1.5b','llama3:latest']
    
#     response = LocalClient().chat(
#         model=model,
#         messages=[
#             {"role": "user", "content": text},
#         ],
#     )
#     return response["message"]["content"]

def completion_with_ollama(text: str, model: str = "phi3:mini") -> str:
    
    response = LocalClient().generate(
        model=model,
        messages=text
    )
    if response:
        return response["response"]
    else: 
        return "Error with the remoteclient"

def completion_with_ollama_remote(text: str, system: str = "") -> str:
    
    response = RemoteClient().generate(
        system=system,
        messages=text
    )
    if response:
        return response["response"]
    else: 
        return "Error with the remoteclient"

def completion_with_chatgpt(text: str, 
                            model: str = "phi3:mini",
                            system:str="You are a helpful assistant.",
                            is_local: bool = True,
                            is_openai: bool = False) -> str:


    if is_local:
        return completion_with_ollama(text, model)
        
    else:
        return completion_with_ollama_remote(text, system)


