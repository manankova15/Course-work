import json
from xml.etree.ElementTree import Element, SubElement, tostring
import xml.dom.minidom

def convert_problem(lti_data):
    quiz = Element('quiz')

    for problem in lti_data['problems']:
        question = SubElement(quiz, 'question', {'type': 'coderunner'})

        name = SubElement(question, 'name')
        text = SubElement(name, 'text')
        problem_name_dict = problem['problem_name']
        problem_name = problem_name_dict.get('en', problem_name_dict.get('ru', next(iter(problem_name_dict.values()), '')))
        text.text = problem_name

        questiontext = SubElement(question, 'questiontext', {'format': 'html'})
        question_text = SubElement(questiontext, 'text')
        question_description = problem['problem_description']
        # Create a CDATA section without encoding special characters
        cdata = '<![CDATA[{}]]>'.format(question_description)
        question_text.text = cdata

        generalfeedback = SubElement(question, 'generalfeedback', {'format': 'html'})
        generalfeedback_text = SubElement(generalfeedback, 'text')
        generalfeedback_text.text = ''

        defaultgrade = SubElement(question, 'defaultgrade')
        defaultgrade.text = '1.0000000'

        penalty = SubElement(question, 'penalty')
        penalty.text = '0.0000000'

        hidden = SubElement(question, 'hidden')
        hidden.text = '0'

        idnumber = SubElement(question, 'idnumber')
        idnumber.text = ''

        coderunnertype = SubElement(question, 'coderunnertype')
        coderunnertype.text = 'python3'

        # Add other elements here with empty text if needed

        testcases = SubElement(question, 'testcases')

        for test_case in problem['test_cases']:
            testcase = SubElement(testcases, 'testcase', {
                'testtype': '0',
                'useasexample': '0',
                'hiderestiffail': '1',
                'mark': '1.0000000'
            })

            testcode = SubElement(testcase, 'testcode')
            testcode_text = SubElement(testcode, 'text')
            testcode_text.text = ''

            stdin = SubElement(testcase, 'stdin')
            stdin_text = SubElement(stdin, 'text')
            stdin_text.text = test_case['input']

            expected = SubElement(testcase, 'expected')
            expected_text = SubElement(expected, 'text')
            expected_text.text = test_case['expected_output']

            extra = SubElement(testcase, 'extra')
            extra_text = SubElement(extra, 'text')
            extra_text.text = ''

            display = SubElement(testcase, 'display')
            display_text = SubElement(display, 'text')
            display_text.text = 'HIDE'  # Assuming it's always hidden in smartlms

    return quiz

def call_converter_to_lms(uploaded_file):
    lti_json = json.loads(uploaded_file.read())
    lms_xml = convert_problem(lti_json)
    return lms_xml

