import os
from routellm.controller import Controller
import time
from dotenv import load_dotenv
##to load credentials
load_dotenv()


os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
os.environ["GEMINI_API_KEY"] = os.getenv("GEMINI_API_KEY")

model_names = ['groq/llama3-70b-8192', 'gemini/gemini-1.5-flash', 'gpt-3.5-turbo', 'gpt-4o']

class Router:
    def __init__(self, temperature=0.3, cost_threshold='0.14869'):
        self.temperature = temperature
        self.cost_threshold = float(cost_threshold)
        self.router_model = f"router-mf-{cost_threshold}"
        self.max_tokens = 4096
        self.strong_model = None
        self.weak_model = None


    def _routed_model(self, weak_model, strong_model, history):
        client = Controller(
            # By default, Controller uses the best performing configuration.
            routers=["mf"],
            strong_model= strong_model,
            weak_model=weak_model
            )

        ## Extract all user comments
        prompt_list = [conv['content'] for conv in history if conv['role']=='user']
        prompt = ".".join(prompt_list)
        print("Prompt: ", prompt)
        routed_model = client.route(prompt=prompt, router="mf", threshold=self.cost_threshold)
        return routed_model

    def select_cheapest_model(self, history):
        chosen_model = None
        ## Iteratively find the weak and strong model
        for index in range(len(model_names) -1):
            weak_model = model_names[index]
            strong_model = model_names[index+1]

            routed_model = self._routed_model(weak_model, strong_model, history)

            if routed_model == weak_model:
                self.strong_model = strong_model
                self.weak_model = weak_model
                chosen_model = routed_model
                return chosen_model

        ## If weak model is never chosen, run the strongest model
        self.strong_model = model_names[-1]
        self.weak_model = model_names[-2]
        chosen_model = self.strong_model    
        return chosen_model

    def generate(self, history):

        ## Generate completion

        t1 = time.time()
        chosen_model = self.select_cheapest_model(history)
        t2 = time.time()

        print(f"Time to chose the cheapest model is {t2-t1} and it is {chosen_model}")

        client = Controller(
        routers=["mf"],
        strong_model= self.strong_model,
        weak_model= self.weak_model
        )


        chat_completion = client.chat.completions.create(
        # This tells RouteLLM to use the MF router with a cost threshold of 0.11593
        model=self.router_model,
        temperature = self.temperature,
        max_tokens = self.max_tokens, 
        messages=history)

        model_response = chat_completion.choices[0].message.content
        model_used = chat_completion.model
        print(model_response, model_used)
        return model_response, model_used

        