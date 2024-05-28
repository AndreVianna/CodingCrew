"""
represents the node where the user is prompted to answer additional questions to refine the project description.

Args:
    state (AnalysisState): The current state of the analysis.

Returns:
    AnalysisState: The updated state after querying the user.
"""

import sys
from textwrap import dedent

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
    print(dedent("""
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
            proposal = ""
            if (question['proposal'] is not None and question['proposal'] != ''):
                proposal = dedent(f"""
                            Analyst Proposed Answer:
                            {question['proposal']}
                            """)
            prompt = dedent(f"""
                                Question {count} of {total}
                                {question['text']}{proposal}
                                Answer:""")
            print(prompt)
            line = ""
            while True:
                try:
                    line = input()
                    if line == 'EXIT':
                        sys.exit(0)
                    if line == 'N/A':
                        answer = 'This question is not applicable to the project.'
                        line=""
                        break
                    if line == 'OK':
                        answer = ""
                        line=""
                        break
                    if line == 'SKIP':
                        skip = True
                        answer = ""
                        line=""
                        break
                    if line == 'FINISH':
                        skip = True
                        finish = True
                        answer = ""
                        line=""
                        break
                except EOFError:
                    break
            answer += f"{line}\n"
        answer = str(answer or "").strip()
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
