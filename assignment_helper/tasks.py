from crewai import Task
from textwrap import dedent


class AssignmentWritingTasks:

    def generate_ideas(self, agent, task):
        return Task(
            description=dedent(
            f"""
            Users task is below. Use the search tools you have to generate ideas for the report. Only generate ideas.
            {task}
            """
            ),
            agent=agent,
        )

    def write_report(self, agent, task):
        return Task(
            description=dedent(
            f"""
            Use the ideas from the idea generator to now write a report for the student task below. 
            {task} 
            """
            ),
            agent=agent,
        )

    def evaluate_report(self, agent, task):
        return Task(
            description=dedent(
            f"""
            Users task is below. Review the report written and provide opportunities for improvement. Check it against your rubric
            {task} 
            """
            ),
            agent=agent,
        )
    
    def rewrite_report(self, agent, task):
        return Task(
            description=dedent(
            f"""
            Users task is below. Review the initial report and the feedback from the report critic to rewrite addressing the feedback
            {task} 
            """
            ),
            agent=agent,
        )