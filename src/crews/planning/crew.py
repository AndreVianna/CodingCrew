"""Email filter crew."""

from crewai import Crew

from crews.planning.agents import PlanningAgents
from crews.planning.tasks import PlanningTasks
from workflows.planning.states import InitialAnalysisResult

class PlanningCrew():
    def __init__(self):
        agents = PlanningAgents()
        self.system_analyst = agents.system_analyst()

    def kickoff(self, state):
        tasks = PlanningTasks()
        crew = Crew(
            agents=[self.system_analyst],
            tasks=[
                tasks.initial_analysis(self.system_analyst, state),
            ],
            verbose=True
        )
        response = crew.kickoff()
        result = InitialAnalysisResult.from_json(response)
        return {
            **state,
            "project_description": result.updated_description,
            "context": {
                "questions": result.additional_questions,
            }
        }
