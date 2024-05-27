"""Email filter crew."""

from crewai import Crew

from crews.agents import PlanningAgents
from crews.tasks import PlanningTasks
from crews.models import CrewOutput
from workflows.states import AnalysisState

class AnalysisCrew():
    """
    Represents a crew responsible for analysis tasks.

    Attributes:
        system_analyst: The system analyst agent assigned to the crew.
    """

    def __init__(self):
        agents = PlanningAgents()
        self.system_analyst = agents.system_analyst()

    def kickoff(self, state: AnalysisState) -> AnalysisState:
        """
        Kick off the crew's analysis process.

        Args:
            state (AnalysisState): The initial state of the analysis.

        Returns:
            AnalysisState: The updated state of the analysis after the crew's kickoff.

        """
        tasks = PlanningTasks()
        crew = Crew(
            agents=[self.system_analyst],
            tasks=[
                tasks.initial_analysis(self.system_analyst, state),
            ],
            verbose=True
        )
        response = crew.kickoff()
        result = CrewOutput.from_json(response)
        return {
            **state,
            "project_description": result.description,
            "questions": result.questions,
        }

class ReportingCrew():
    """
    A crew responsible for generating a final report based on the analysis state.

    Attributes:
        system_analyst: The system analyst agent responsible for analyzing the system.
    """

    def __init__(self):
        agents = PlanningAgents()
        self.system_analyst = agents.system_analyst()

    def kickoff(self, state: AnalysisState) -> AnalysisState:
        """
        Kick off the crew's analysis process.

        Args:
            state (AnalysisState): The initial analysis state.

        Returns:
            AnalysisState: The updated analysis state with the final report.

        """
        tasks = PlanningTasks()
        crew = Crew(
            agents=[self.system_analyst],
            tasks=[
                tasks.final_report(self.system_analyst, state),
            ],
            verbose=True
        )
        response = crew.kickoff()
        with open("report.md", "w", encoding="utf-8") as file:
            file.write(response)
        return {
            **state,
            "final_report": response,
        }
