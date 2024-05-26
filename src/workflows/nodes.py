"""Nodes for the planing workflow."""

from textwrap import dedent

from common import Query
from workflows.states import AnalysisState
from common import Query, Question

class PlanningNodes():
    def start_project(self, state: AnalysisState):
        # project_name = input("Enter the project name: ")
        # project_description = input("Enter the project description: ")
        project_name = "FacePuppy"
        project_description = "FacePuppy is a social media web application dedicated to dog owners. It is created using Flutter/Dart and Node.js/Angular. Users can register their puppies, create profiles, upload photos, and share blog posts. User interaction is encouraged through a search and follow feature, allowing users to search for puppies by name, breed, color, size, etc., and follow profiles they are interested in. Notifications are managed through an in-app alert system, with an optional real-time email alert system that users can unsubscribe from through a link in the email or via their profile on the site. The application is designed with a modern, clean aesthetic using a light blue and light green color scheme. There are three user roles - Guest, User, and Administrator - each with varying permissions. Guests only have access to the public areas of the site. Registered users have access to all functionalities except administration actions, while administrators have access to everything, including managing users and puppies, responding to contact requests, and moderating blog posts and comments to prevent inappropriate content. The application is responsive and hosted on Azure. Currently, there are no specific performance, backup, recovery, or regulatory requirements. User data deletion requests will be handled in adherence to GDPR or similar regulations."
        return {
            **state,
            'project_name': project_name,
            'project_description': project_description,
        }
    
    def query_user(self, state: AnalysisState):
        if state['questions'] is None or state['questions'] == []:
            return {
                **state,
                'questions': None,
                'finish': True,
            }
        queries = state['queries'] or list[Query]()
        total = len(state['questions'])
        count = 0
        skip = False
        finish = False
        print(dedent("""
                     Here are some addtional questions.
                     Please answer them to refine the project description.
                     To mark the answer as not applicable, type 'N/A'. (The question will be marked as answered as not applicable to the project.)
                     To accept the analyst proposal to that question type 'ACCEPT' or 'OK' or just press [enter]. (The question will be marked as answered by the analyst.)
                     To finish the questionary type 'SKIP'. (All the remaining questions will be marked as answered by the analyst.)
                     To finish the analysis type 'FINISH'. (All the remaining questions will be marked as answered by the analyst ans no more questions will be generated ending the analysis.)
                     """))
        for question in state['questions']:
            skip=finish
            count += 1
            query = Query()
            query['question'] = question['text'],
            query['answer'] = None,
            if not skip:
                proposal = ""
                if (question['proposal'] is not None and question['proposal'] != ''):
                    proposal = f"""
                                Analyst Proposal:
                                {question['proposal']}
                                """
                         
                prompt = dedent(f"""
                                 Question {count} ot {total}
                                 {question['text']}{proposal}
                                 Answer:
                                 """)
                query['answer'] = input(prompt)
            if query['answer'] == 'N/A':
                query['answer'] = 'This question is not applicable to the project67yumjk.',
            if query['answer'] == 'FINISH':
                finish = True
                query['answer'] = 'SKIP'
            if query['answer'] is None or query['answer'] == 'SKIP' or query['answer'] == '':
                skip = True
            if skip:
                query['answer'] = question['proposal'] or 'The analyst can propose the answer to this question.',
            queries.append(query)
        if not finish:
            
            finish = (input("Finish the analisys? (yes/[no]): ") or "n")[0].lower == 'y',
        return {
            **state,
            'queries': queries,
            'finish': finish,
        }

    def has_answers(self, state: AnalysisState):
        if state['questions'] is None or state['questions'] == []:
            return "FINISH"
        return "CONTINUE"
