from ..models.project_state import ProjectState
from ..tasks.generate_questions_task import GenerateQuestionsTask

def create(state: ProjectState) -> ProjectState:
    task = GenerateQuestionsTask()
    return task.execute(state)