import json

def get_converted_json(parsed_json):
    result = {}

    if parsed_json.get("problem_type", None) != None:
        result["problem_type"] = parsed_json.get("problem_type")
    else:
        result["problem_type"] = "problemWithChecker"

    result["id"] = parsed_json.get("id")

    result["correct_solution_code"] = parsed_json.get("source", {}).get("code", "")

    result["problem_description"] = parsed_json.get("block", {}).get("text", "")

    result["required_files"] = {
        "input_file": None,
        "output_file": None,
        "redirect_stdin": True,
        "redirect_stdout": True
    }

    result["solution_code_template"] = {
        "python3": parsed_json.get("options", {}).get("code_templates", {}).get("python3", ""),
        "kotlin": parsed_json.get("options", {}).get("code_templates", {}).get("kotlin", ""),
        "c++": None
    }

    result["problem_name"] = {
        "ru": None,
        "en": None
    }

    result["constraints"] = {
        "execution_time_limit_sec": parsed_json.get("options", {}).get("execution_time_limit"),
        "execution_memory_limit": parsed_json.get("options", {}).get("execution_memory_limit"),
        "output_limit": None
    }

    result["answer_format"] = {
        "type": "text",
        "max_source_size_kb": None,
        "pattern": None
    }

    result["execution_constraints"] = {
        "time_limit_seconds": None,
        "idleness_limit_millis": None,
        "memory_limit_mb": None,
        "output_limit": None,
        "private_constraints": {
            "python3": {
                "time_limit_seconds": parsed_json.get("options", {}).get("limits", {}).get("python3", {}).get("time"),
                "memory_limit_mb": parsed_json.get("options", {}).get("limits", {}).get("python3", {}).get("memory")
            },
            "kotlin": {
                "time_limit_seconds": parsed_json.get("options", {}).get("limits", {}).get("kotlin", {}).get("time"),
                "memory_limit_mb": parsed_json.get("options", {}).get("limits", {}).get("kotlin", {}).get("memory")
            }
        }
    }

    result["compilation_constraints"] = {
        "time_limit_seconds": None,
        "idleness_limit_millis": None,
        "memory_limit_mb": None,
        "output_limit": None
    }

    result["file_tests"] = []

    result["test_cases"] = []

    result["checker_settings"] = {
        "checker_type": None,
        "limits": {
            "time_limit_seconds": None,
            "idleness_limit_millis": None,
            "memory_limit_mb": None,
            "output_limit": None
        }
    }

    return result

def convert_stepic_to_lti(path):
    with open(path, 'r', encoding='utf-8') as file:
        stepik_json = json.load(file)

    lti_json = get_converted_json(stepik_json)

    return lti_json

def call_converter_from_stepic():
    lti_json = convert_stepic_to_lti('/Users/manankova15/Desktop/курсач/степик.step')
    print(json.dumps(lti_json, indent=4, ensure_ascii=False).encode('utf-8').decode())
    print("___________________________________________________")
