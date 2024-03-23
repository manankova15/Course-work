import xml.etree.ElementTree as ET
import json
from langdetect import detect


def convert_problem(xml_file):
    # tree = ET.parse(xml_file)
    # root = tree.getroot()

    root = ET.fromstring(xml_file)

    lti_format = {"problems": []}

    questions = root.findall('.//question[@type="coderunner"]')

    for question in questions:
        problem = {}
        problem["problem_type"] = question.get('type')

        # Получаем значение атрибута idnumber
        question_id = question.findtext("./comment")
        problem["id"] = question_id

        problem["code_for_testing"] = ""

        problem_description = question.find('.//questiontext').find('text').text
        problem["problem_description"] = problem_description

        problem["required_files"] = {
            "input_file": None,
            "output_file": None,
            "redirect_stdin": True,
            "redirect_stdout": True
        }
        problem["code_template"] = {}
        problem_name = question.find('.//name').find('text').text

        languages_to_check_first = ['ru', 'en']
        for lang in languages_to_check_first:
            if lang in detect(problem_name):
                language = lang
                break
        else:
            language = detect(problem_name)

        problem["problem_name"] = {
            language: problem_name
        }

        problem["execution_constraints"] = {
            "time_limit_seconds": None,
            "idleness_limit_millis": None,
            "memory_limit_mb": None,
            "output_limit": None,
            "private_constraints": {}
        }
        problem["compilation_constraints"] = {
            "time_limit_seconds": None,
            "idleness_limit_millis": None,
            "memory_limit_mb": None,
            "output_limit": None
        }

        problem["file_tests"] = []

        test_cases = []
        for testcase in question.findall('.//testcase'):
            input_data = testcase.find('.//stdin').find('.//text').text.strip()
            expected_output = testcase.find('.//expected').find('.//text').text.strip()
            test_cases.append({"input": input_data, "expected_output": expected_output})

        problem["test_cases"] = test_cases

        problem["checker_settings"] = {
            "checker_type": "standardChecker",
            "limits": {
                "time_limit_seconds": None,
                "idleness_limit_millis": None,
                "memory_limit_mb": question.find('.//memlimitmb', None).text,
                "output_limit": None
            }
        }

        lti_format["problems"].append(problem)

    return lti_format

def call_converter_from_lms(uploaded_file):
    lms_json = uploaded_file.read()
    lti_json = convert_problem(lms_json)
    return lti_json
