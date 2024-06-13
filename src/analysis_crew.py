"""
Represents a crew responsible for analysis tasks.

Attributes:
    execute_initial_analysis: The method to execute the initial analysis.
    generate_report: The method to generate the final report.
"""

import asyncio
import sys
# from typing import List, Tuple, Union
import uuid
from crewai import Crew, Agent, Process
# from crewai.tasks.task_output import TaskOutput
# from langchain_core.agents import AgentFinish, AgentAction
from langchain_openai import ChatOpenAI
# from pydantic import UUID4

from utils.terminal import terminal


from agents import system_analyst     #, report_writer
from tasks import update_description  #, generate_questions, generate_report,
from tasks.models import ProjectState #, Query

class AnalysisCrew:
    """
    Represents a crew responsible for executing the analysis and updating the project description.

    Attributes:
        system_analyst (SystemAnalyst): The system analyst agent.

    Methods:
        execute_analysis(state: ProjectState) -> ProjectState:
            Kick off the crew's analysis process.

        generate_report(state: ProjectState) -> ProjectState:
            Kick off the report generation process.
    """
    is_debugging: bool

    system_analyst: Agent
    report_writer: Agent

    def __init__(self, is_debugging: bool):
        self.is_debugging = is_debugging

        self.system_analyst = system_analyst.create(is_debugging)
        # self.report_writer = report_writer.create(is_debugging)

    async def execute_analysis(self, state: ProjectState) -> ProjectState:
        """
        Kick off the crew's analysis process.

        Args:
            state (ProjectState): The initial state of the analysis.

        Returns:
            ProjectState: The updated state of the analysis after the crew's kickoff.

        """
        terminal.write_line("Setting up crew...")
        update_description_task = update_description.create(self.system_analyst, state)

        # def step_callback(step: Union[AgentFinish, List[Tuple[AgentAction, str]]]) -> None:
        #     if isinstance(step, AgentFinish):
        #         terminal.write_line("Step completed.")
        #         terminal.write_line(f"Result: {step}")
        #     else:
        #         step_count = 1
        #         for action, observation in step:
        #             terminal.write_line(f"Step {step_count}:")
        #             terminal.write_line(f"Observaltion: {observation}")
        #             terminal.write_line(f"Result: {action}")
        #             step_count += 1

        # def task_callback(task: TaskOutput) -> None:
        #     terminal.write_line()
        #     terminal.write_line("Task completed.")
        #     terminal.write_line(f"Result: {task.raw_output}")
        #     terminal.write_line()

        terminal.write_line("Create crew...")
        crew = Crew(
            id=uuid.uuid4(),
            agents=[self.system_analyst],
            tasks=[update_description_task],
            verbose=self.is_debugging,
            memory=True,
            process=Process.hierarchical,
            llm=ChatOpenAI(model_name="gpt-4o", temperature=0),
            manager_llm=ChatOpenAI(model_name="gpt-4o", temperature=0),
            output_log_file="./logs/analysis.log",
            # task_callback=task_callback,
            # step_callback=step_callback,
        )
        terminal.write_line("Starting crew for project analysis...")
        terminal.write_line()

        try:
            response = await terminal.wait_for(crew.kickoff(), text="Thinking...", timeout=30)
        except asyncio.TimeoutError:
            terminal.write_line()
            terminal.write_line("Crew work was stopped because it was taking too long to complete.")
            terminal.write_line("Please try again later.")
            sys.exit(1)

        terminal.write_line()
        terminal.write_line("Analysis completed.")
        return {
            **state,
            "updated_description": response,
        }

    # async def generate_report(self, state: ProjectState) -> ProjectState:
    #     """
    #     Kick off the report generation process.

    #     Args:
    #         state (ProjectState): The current state of the analysis.

    #     Returns:
    #         ProjectState: The updated analysis state with the content of the final report.

    #     """
    #     crew = Crew(
    #         agents=[self.report_writer],
    #         tasks=[
    #             generate_project_summary.create(self.report_writer, state),
    #         ],
    #         verbose=self.is_debugging,
    #     )
    #     terminal.write_line("Generating report...")
    #     terminal.write_line()

    #     try:
    #         response = await terminal.wait_for(crew.kickoff(), text="Writing...", timeout=30)
    #     except asyncio.TimeoutError:
    #         terminal.write_line()
    #         terminal.write_line("The report generation process took too long to complete.")
    #         terminal.write_line("Please try again later.")
    #         return state

    #     terminal.write_line()
    #     terminal.write_line("Reported generated.")
    #     with open("report.md", "w", encoding="utf-8") as file:
    #         file.write(response)
    #     return {
    #         **state,
    #         "final_report": response,
    #     }
