import json

def decode_unicode(json_data):
    if isinstance(json_data, dict):
        decoded_dict = {}
        for key, value in json_data.items():
            decoded_dict[key] = decode_unicode(value)
        return decoded_dict
    elif isinstance(json_data, list):
        return [decode_unicode(item) for item in json_data]
    elif isinstance(json_data, str):
        return json_data.encode('utf-8').decode('unicode-escape')
    else:
        return json_data


def get_problem(yandex_json):
    if "problemMetadata" in yandex_json:
        yandex_json = yandex_json.get("problemMetadata", {})

    lti_json = {}

    if yandex_json.get("problemTypeMeta", None) != None:
        lti_json["problem_type"] = yandex_json.get("problemTypeMeta", "WITH_CHECKER")
    elif yandex_json.get("__type", None) != None:
        lti_json["problem_type"] = yandex_json.get("__type", "WITH_CHECKER")

    lti_json["id"] = yandex_json.get("id", None)
    lti_json["correct_solution_code"] = yandex_json.get("solutions", None)
    if yandex_json.get("statements", None) is not None and len(yandex_json.get("statements", None)) > 0:
        lti_json["problem_description"] = yandex_json.get("statements", None)[0].get("markdownStatement", None).get(
            "legend", None)
    else:
        lti_json["problem_description"] = None

    required_files = yandex_json.get("fileSet", {})
    lti_json["required_files"] = {
        "input_file": required_files.get("inputFile", None),
        "output_file": required_files.get("outputFile", None),
        "redirect_stdin": required_files.get("redirectStdin", None),
        "redirect_stdout": required_files.get("redirectStdout", None),
    }

    lti_json["solution_code_template"] = None

    lti_json["problem_name"] = yandex_json.get("names", None)

    solution_limits = yandex_json.get("solutionLimits", {})

    lti_json["execution_constraints"] = {
        "time_limit_seconds": int(solution_limits.get("timeLimitMillis", 0)) / 1000 if solution_limits.get(
            "timeLimitMillis", None) != None else None,
        "idleness_limit_millis": solution_limits.get("idlenessLimitMillis", None),
        "memory_limit_mb": int(solution_limits.get("memoryLimit", 0)) / (1024 * 1024) if solution_limits.get(
            "memoryLimit", None) != None else None,
        "output_limit": solution_limits.get("outputLimit", None),
        "private_constraints": {}
    }

    compilation_limits = yandex_json.get("compilationLimits", {})
    lti_json["compilation_constraints"] = {
        "time_limit_seconds": int(compilation_limits.get("timeLimitMillis", 0)) / 1000 if compilation_limits.get(
            "timeLimitMillis", None) != None else None,
        "idleness_limit_millis": compilation_limits.get("idlenessLimitMillis", None),
        "memory_limit_mb": compilation_limits.get("memoryLimit", None),
        "output_limit": compilation_limits.get("outputLimit", None)
    }

    public_tests = []
    for test_set in yandex_json.get("testSets", []):
        tests = []
        for test in test_set.get("matchedTests", []):
            tests.append({
                "input_path": test.get("inputPath", None),
                "answer_path": test.get("answerPath", None),
                "input_exists": test.get("inputExists", False),
                "answer_exists": test.get("answerExists", False)
            })
        public_tests.append({
            "name": test_set.get("name", None),
            "input_file_pattern": test_set.get("inputFilePattern", None),
            "answer_file_pattern": test_set.get("answerFilePattern", None),
            "tests": tests
        })

    lti_json["file_tests"] = public_tests

    lti_json["test_cases"] = []

    checker_settings = yandex_json.get("checkerSettings", {})
    lti_json["checker_settings"] = {
        "checker_type": checker_settings.get("checkerType", None),
        "limits": {
            "time_limit_millis": int(
                checker_settings.get("limits", {}).get("timeLimitMillis", 0)) if checker_settings.get("limits", {}).get(
                "timeLimitMillis", None) != None else None,
            "idleness_limit_millis": checker_settings.get("limits", {}).get("idlenessLimitMillis", None),
            "memory_limit_mb": checker_settings.get("limits", {}).get("memoryLimit", None),
            "output_limit": checker_settings.get("limits", {}).get("outputLimit", None)
        },
    }

    return lti_json


def convert_yandex_to_lti(uploaded_file):
    yandex_json = json.loads(uploaded_file.read())

    lti_json = []
    if "problems" in yandex_json:
        list_of_problems = yandex_json.get("problems")
        for problem in list_of_problems:
            lti_json.append(get_problem(problem))
    else:
        lti_json.append(get_problem(yandex_json))

    return {"problems": lti_json}


def call_converter_from_yandex(uploaded_file):
    lti_json = convert_yandex_to_lti(uploaded_file)
    return lti_json
    # lti_json = convert_yandex_to_lti('/Users/manankova15/Desktop/курсач/яндекс.json')
    # print(json.dumps(lti_json, indent=4, ensure_ascii=False).encode('utf-8').decode())
    # print("___________________________________________________")
    #
    # lti_json = convert_yandex_to_lti('/Users/manankova15/Desktop/курсач/yandex_ful.json')
    # print(json.dumps(lti_json, indent=4, ensure_ascii=False).encode('utf-8').decode())
    # print("___________________________________________________")
    #
    # lti_json = convert_yandex_to_lti('/Users/manankova15/Desktop/курсач/meta.json')
    # print(json.dumps(lti_json, indent=4, ensure_ascii=False).encode('utf-8').decode())

    # print(json.dumps(lti_json, indent=4, ensure_ascii=False).encode('utf-8').decode())

