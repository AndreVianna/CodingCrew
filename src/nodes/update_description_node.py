from ..models.project_state import ProjectState
from ..tasks.update_description_task import UpdateDescriptionTask

def create(state: ProjectState) -> ProjectState:
    task = UpdateDescriptionTask()
    return task.execute(state)