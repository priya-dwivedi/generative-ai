import os
from crewai import Crew

from textwrap import dedent
from agents import AssignmentHelperAgents
from tasks import AssignmentWritingTasks

from dotenv import load_dotenv
load_dotenv()

print("## Welcome to the Assignment Writer Crew")
print('-------------------------------')
task_description = input("What kind of Assignment do you need help with? Share more details about the task, which grade it is for and any considerations \n")


agents = AssignmentHelperAgents()
tasks = AssignmentWritingTasks()

## Instantiate the agents
idea_generator_agent = agents.IdeaGeneratorAgent()
writer_agent = agents.ReportWriterAgent()
evaluator_agent = agents.ReportEvaluatorAgent()


## Instantiate the tasks
generate_ideas = tasks.generate_ideas(idea_generator_agent, task_description)
write_report = tasks.write_report(writer_agent, task_description)
evaluate_report = tasks.evaluate_report(evaluator_agent, task_description)
rewrite_report = tasks.rewrite_report(writer_agent, task_description)


### Step 1 - Get the course intro and course module output
crew_startup = Crew(
    agents=[idea_generator_agent, writer_agent, evaluator_agent ],
    tasks=[generate_ideas, write_report, evaluate_report, rewrite_report],
    verbose=True,
    full_output=True
)

        ## Step 2 - Parse the above output to extract modules. Store the intro in a JSON under Intro.
        ## Step 3 - Iterate over each module and launch the second crew consisting of 1. Writer, Critic, Rewriter, Quiz Generator
        ## As each module gets done, store it in the final output JSON
        ## Step 4 - Call the summarizer of the course. We should pass to it the JSON containing all the course modules. 


result = crew_startup.kickoff()
print("\n\n########################")
print("## Run Result:")
print("########################\n")
print(result)

