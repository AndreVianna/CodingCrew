"""Nodes for the planing workflow."""

from textwrap import dedent

from workflows.states import AnalysisState
from common import Query

class PlanningNodes():
    """
    This class represents a set of planning nodes used in the workflow.
    """

    def start_project(self, state: AnalysisState):
        """
        Prompts the user to enter the project name and description, and updates the state accordingly.

        Args:
            state (AnalysisState): The current state of the analysis.

        Returns:
            dict: The updated state with the project name and description added.
        """
        project_name = input("Enter the project name: ")
        project_description = input("Enter the project description: ")
        return {
            **state,
            'project_name': project_name,
            'project_description': project_description,
        }

    def query_user(self, state: AnalysisState):
        """
        Queries the user for additional information to refine the project description.

        Args:
            state (AnalysisState): The current state of the analysis.

        Returns:
            dict: The updated state after querying the user.

        """
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
                     Here are some additional questions.
                     Please answer them to refine the project description.
                     To mark the answer as not applicable, type 'N/A'. (The question will be marked as answered as not applicable to the project.)
                     To accept the analyst proposal to that question type 'ACCEPT' or 'OK' or just press [enter]. (The question will be marked as answered by the analyst.)
                     To finish the questionnaire type 'SKIP'. (All the remaining questions will be marked as answered by the analyst.)
                     To finish the analysis type 'FINISH'. (All the remaining questions will be marked as answered by the analyst and no more questions will be generated, ending the analysis.)
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
                                 Question {count} of {total}
                                 {question['text']}{proposal}
                                 Answer:
                                 """)
                query['answer'] = input(prompt)
            if query['answer'] == 'N/A':
                query['answer'] = 'This question is not applicable to the project.',
            if query['answer'] == 'FINISH':
                finish = True
                query['answer'] = 'SKIP'
            if query['answer'] is None or query['answer'] == 'SKIP' or query['answer'] == '':
                skip = True
            if skip:
                query['answer'] = question['proposal'] or 'The analyst can propose the answer to this question.',
            queries.append(query)
        if not finish:
            yes_no = input("Finish the analysis? (yes/[no]): ")
            finish = (yes_no or "n")[0].lower == "y",
        return {
            **state,
            'queries': queries,
            'finish': finish,
        }

    def has_answers(self, state: AnalysisState):
        """
        Checks if there are any unanswered questions in the given state.

        Args:
            state (AnalysisState): The state containing the questions.

        Returns:
            str: "FINISH" if there are no questions or "CONTINUE" if there are unanswered questions.
        """
        if state['questions'] is None or state['questions'] == []:
            return "FINISH"
        return "CONTINUE"
