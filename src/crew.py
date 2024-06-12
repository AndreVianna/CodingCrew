"""
Represents a crew responsible for analysis tasks.

Attributes:
    execute_initial_analysis: The method to execute the initial analysis.
    generate_report: The method to generate the final report.
"""

import asyncio
from crewai import Crew
from langchain_openai import ChatOpenAI

from utils.terminal import terminal

from .agents import system_analyst, report_writer
from .tasks import execute_analysis, generate_project_summary_report
from .models.crew import CrewOutput
from .models.workflow import AnalysisState



class ProjectCrew:
    """
    Represents a crew responsible for executing the analysis and generating reports for a project.

    Attributes:
        system_analyst (SystemAnalyst): The system analyst agent.
        report_writer (ReportWriter): The report writer agent.

    Methods:
        execute_initial_analysis(state: AnalysisState) -> AnalysisState:
            Kick off the crew's analysis process.

        generate_report(state: AnalysisState) -> AnalysisState:
            Kick off the report generation process.
    """

    def __init__(self, is_debugging: bool):
        self.system_analyst = system_analyst.create(is_debugging)
        self.report_writer = report_writer.create(is_debugging)
        self.is_debugging = is_debugging

    async def execute_analysis(self, state: AnalysisState) -> AnalysisState:
        """
        Kick off the crew's analysis process.

        Args:
            state (AnalysisState): The initial state of the analysis.

        Returns:
            AnalysisState: The updated state of the analysis after the crew's kickoff.

        """
        crew = Crew(
            agents=[self.system_analyst],
            tasks=[
                execute_analysis.create(self.system_analyst, state),
            ],
            verbose=self.is_debugging,
            llm=ChatOpenAI(model_name="gpt-4o", temperature=0),
            manager_llm=ChatOpenAI(model_name="gpt-4o", temperature=0),
        )
        terminal.write_line("Starting the analysis process...")
        terminal.write_line()

        try:
            response = await terminal.wait_for(crew.kickoff(), text="Thinking...", timeout=30)
        except asyncio.TimeoutError:
            terminal.write_line()
            terminal.write_line("The analysis process took too long to complete.")
            terminal.write_line("Please try again later.")
            return state

        terminal.write_line()
        terminal.write_line("Analysis completed.")
        result = CrewOutput.from_json(response)
        return {
            **state,
            "project_description": result.description,
            "questions": result.questions,
        }

    async def generate_report(self, state: AnalysisState) -> AnalysisState:
        """
        Kick off the report generation process.

        Args:
            state (AnalysisState): The current state of the analysis.

        Returns:
            AnalysisState: The updated analysis state with the content of the final report.

        """
        crew = Crew(
            agents=[self.report_writer],
            tasks=[
                generate_project_summary_report.create(self.report_writer, state),
            ],
            verbose=self.is_debugging,
        )
        terminal.write_line("Generating report...")
        terminal.write_line()

        try:
            response = await terminal.wait_for(crew.kickoff(), text="Writing...", timeout=30)
        except asyncio.TimeoutError:
            terminal.write_line()
            terminal.write_line("The report generation process took too long to complete.")
            terminal.write_line("Please try again later.")
            return state

        terminal.write_line()
        terminal.write_line("Reported generated.")
        with open("report.md", "w", encoding="utf-8") as file:
            file.write(response)
        return {
            **state,
            "final_report": response,
        }
