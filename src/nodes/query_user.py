"""
represents the node where the user is prompted to answer additional questions to refine the project description.

Args:
    state (AnalysisState): The current state of the analysis.

Returns:
    AnalysisState: The updated state after querying the user.
"""

import sys
from utils import read_text, outdent, write_line
from models.common import Query
from models.workflow import AnalysisState

def create(state: AnalysisState) -> AnalysisState:
    """
    Queries the user for additional information to refine the project description.


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
    print(outdent("""
                    Here are some additional questions.
                    Please answer them to refine the project description.
                    - To mark the answer as not applicable, type 'N/A'. (The question will be marked as answered as not applicable to the project.)
                    - To accept the analyst propoed answer type 'OK' or just send an empty answer by pressing <CRTL+ENTER>.
                    - To finish the current questionnaire type 'SKIP'. (All the remaining questions will accept the analyst proposed answer.)
                    = To finish the analysis type 'FINISH'. (All the remaining questions will accept the analyst proposed answer and no more questions will be generated, ending the analysis.)
                    - To terminate the application 'EXIT'.
                    Submit your answer by pressing Ctrl-D or Ctrl-Z on windows.
                    """))
    for question in state['questions']:
        count += 1
        query = Query()
        query['question'] = question['text']
        answer: str = ""
        if not skip:
            proposed_answer = ""
            if (question['proposed_answer'] is not None and question['proposed_answer'] != ''):
                proposed_answer = f"Analyst Proposed Answer:\n{question['proposed_answer']}\n"
            prompt = f"\nQuestion {count} of {total}\n{question['text']}\n{proposed_answer}Answer:\n"
            write_line(prompt)
            lines = read_text()
            answer = ('\n'.join(lines)).strip()
            if answer == 'EXIT':
                sys.exit(0)
            if answer == 'N/A':
                answer = 'This question is not applicable to the project.'
                line=""
                break
            if answer == 'OK':
                answer = ""
                break
            if line == 'SKIP':
                skip = True
                answer = ""
                break
            if line == 'FINISH':
                skip = True
                finish = True
                answer = ""
                break
        if answer == "":
            answer = 'The analyst can propose the answer to this question.'
        query['answer'] = answer
        queries.append(query)
    if not finish:
        yes_no = input("Finish the analysis? (yes/[no]): ")
        print(F"yes/no: {yes_no}")
        first_char = (yes_no or "n")[0].lower()
        print(F"check: {first_char}")
        finish = first_char == "y"
    return {
        **state,
        'queries': queries,
        'finish': finish,
    }
