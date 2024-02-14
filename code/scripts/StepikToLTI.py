import json
import re
from langdetect import detect
def get_converted_json(parsed_json):
    result = {}

    block = parsed_json.get("block", {})

    result["problem_type"] = parsed_json.get("problem_type", "WITH_CHECKER")

    result["id"] = parsed_json.get("id")

    result["code_for_testing"] = block.get("source", {}).get("code", "")

    result["problem_description"] = block.get("text", "")

    result["required_files"] = {
        "input_file": None,
        "output_file": None,
        "redirect_stdin": True,
        "redirect_stdout": True
    }

    result["code_template"] = {}
    templates = block.get("source", {}).get("templates_data", {})
    matches = re.findall(r'::(\w+)(?:\n|$)(.*?)(?=::|\Z)', templates, re.DOTALL)
    for match in matches:
        language = match[0]
        code = match[1].strip()
        result["code_template"][language] = code

    problem_name = block.get("name", "")
    languages_to_check_first = ['ru', 'en']
    for lang in languages_to_check_first:
        if lang in detect(problem_name):
            language = lang
            break
    else:
        language = detect(problem_name)
    result["problem_name"] = {
        language: problem_name
    }

    private_constraints = {}
    limits = block.get("options", {}).get("limits", {})
    for lang, lang_limits in limits.items():
        private_constraints[lang] = {
            "time_limit_seconds": lang_limits.get("time", None),
            "memory_limit_mb": lang_limits.get("memory", None)
        }
    result["execution_constraints"] = {
        "time_limit_seconds": block.get("options", {}).get("execution_time_limit", None),
        "idleness_limit_millis": None,
        "memory_limit_mb": block.get("options", {}).get("execution_memory_limit"),
        "output_limit": None,
        "private_constraints": private_constraints
    }

    result["compilation_constraints"] = {
        "time_limit_seconds": None,
        "idleness_limit_millis": None,
        "memory_limit_mb": None,
        "output_limit": None
    }

    result["file_tests"] = block.get("source", {}).get("test_archive", [])

    result["test_cases"] = block.get("source", {}).get("test_cases", [])

    result["checker_settings"] = {
        "checker_type": None,
        "limits": {
            "time_limit_seconds": None,
            "idleness_limit_millis": None,
            "memory_limit_mb": None,
            "output_limit": None
        }
    }

    return {"problems": [result]}

def convert_stepic_to_lti(path):
    with open(path, 'r', encoding='utf-8') as file:
        stepik_json = json.load(file)

    lti_json = get_converted_json(stepik_json)

    return lti_json

def call_converter_from_stepic():
    lti_json = convert_stepic_to_lti('/Users/manankova15/Desktop/курсач/степик.step')
    print(json.dumps(lti_json, indent=4, ensure_ascii=False).encode('utf-8').decode())
