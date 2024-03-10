import xml.etree.ElementTree as ET
import json

def convert_problem(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    problems = []
    print(root.findall('.//question'))
    for question in root.findall('.//question'):
        problem = {}
        problem['problem_type'] = 'problemWithChecker'
        problem['id'] = question.find('name/text').text.split(':')[1].strip()

        # Extracting problem description
        problem_description = question.find('questiontext/text').text.strip()
        problem['problem_description'] = f"<p>{problem_description}</p>"

        # Extracting input and output files
        problem['required_files'] = {
            "input_file": "input.txt",
            "output_file": "output.txt",
            "redirect_stdin": True,
            "redirect_stdout": True
        }

        # Extracting code template
        problem['code_template'] = {
            "python3": question.find('template').text.strip()
        }

        # Extracting problem name
        problem_name = question.find('name/text').text.strip()
        problem['problem_name'] = {"ru": problem_name, "en": problem_name}

        # Extracting execution constraints
        problem['execution_constraints'] = {
            "time_limit_seconds": float(question.find('cputimelimitsecs').text.strip()),
            "idleness_limit_millis": 10000,
            "memory_limit_mb": float(question.find('memlimitmb').text.strip()),
            "output_limit": 67108864,
            "private_constraints": {
                "python3": {
                    "time_limit_seconds": float(question.find('cputimelimitsecs').text.strip()),
                    "memory_limit_mb": float(question.find('memlimitmb').text.strip())
                }
            }
        }

        # Extracting test cases
        test_cases = []
        for testcase in question.findall('.//testcase'):
            test_input = testcase.find('stdin/text').text.strip()
            expected_output = testcase.find('expected/text').text.strip()

            test_case = {
                "input": test_input,
                "expected_output": expected_output
            }

            test_cases.append(test_case)

        problem['test_cases'] = test_cases

        # Extracting checker settings
        problem['checker_settings'] = {
            "checker_type": "standardChecker",
            "limits": {
                "time_limit_seconds": 10,
                "idleness_limit_millis": 10000,
                "memory_limit_mb": 268435456,
                "output_limit": 268435456
            }
        }

        problems.append(problem)

    return {"problems": problems}

def call_converter_from_lms(uploaded_file):
    stepik_json = json.loads(uploaded_file.read())
    print(stepik_json)
    lti_json = convert_problem(stepik_json)

    print(json.dumps(lti_json, indent=4, ensure_ascii=False).encode('utf-8').decode())

    return lti_json
