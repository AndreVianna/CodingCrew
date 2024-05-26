"""Nodes for the planing workflow."""

from textwrap import dedent

from workflows.planning.states import PlanningState

class PlanningNodes():
    def start_project(self, state):
        # project_name = input("Enter the project name: ")
        # project_description = input("Enter the project description: ")
        project_name = "FacePuppy"
        project_description = "FacePuppy is a social media web application dedicated to dog owners. It is created using Flutter/Dart and Node.js/Angular. Users can register their puppies, create profiles, upload photos, and share blog posts. User interaction is encouraged through a search and follow feature, allowing users to search for puppies by name, breed, color, size, etc., and follow profiles they are interested in. Notifications are managed through an in-app alert system, with an optional real-time email alert system that users can unsubscribe from through a link in the email or via their profile on the site. The application is designed with a modern, clean aesthetic using a light blue and light green color scheme. There are three user roles - Guest, User, and Administrator - each with varying permissions. Guests only have access to the public areas of the site. Registered users have access to all functionalities except administration actions, while administrators have access to everything, including managing users and puppies, responding to contact requests, and moderating blog posts and comments to prevent inappropriate content. The application is responsive and hosted on Azure. Currently, there are no specific performance, backup, recovery, or regulatory requirements. User data deletion requests will be handled in adherence to GDPR or similar regulations."
        return {
            **state,
            'project_name': project_name,
            'project_description': project_description,
        }
    
    def query_user(self, state):
        context = state['context']
        if context is None or 'questions' not in context or context['questions'] == []:
            return {
                **state,
                'context': None,
            }
        queries = []
        questions = context['questions']
        for question in questions:
            query = {
                'question': question,
                'answer': input(dedent(f"""
                                {question}
                                """)),
            }
            queries.append(query)
        return {
            **state,
            'context': {
                'queries': queries,
                'proceed': input("Terminate the analisys? (yes/no): "),
            }
        }

    def has_answers(self, state):
        context = state['context']
        if context is None:
            return "NO"
        return "YES"
