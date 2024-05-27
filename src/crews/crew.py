"""Email filter crew."""

from crewai import Crew

from crews.agents import PlanningAgents
from crews.tasks import PlanningTasks
from crews.models import CrewOutput
from workflows.states import AnalysisState

class AnalysisCrew():
    def __init__(self):
        agents = PlanningAgents()
        self.system_analyst = agents.system_analyst()

    def kickoff(self, state: AnalysisState) -> AnalysisState:
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
    def __init__(self):
        agents = PlanningAgents()
        self.system_analyst = agents.system_analyst()

    def kickoff(self, state: AnalysisState) -> AnalysisState:
        tasks = PlanningTasks()
        crew = Crew(
            agents=[self.system_analyst],
            tasks=[
                tasks.final_report(self.system_analyst, state),
            ],
            verbose=True
        )
        response = crew.kickoff()
        return {
            **state,
            "final_report": response,
        }
