import json


def convert_problem(lti_json):
    yandex_json = {
        "problems": []
    }
    if "problems" in lti_json:
        lti_json = lti_json.get("problems", [])


    for problem in lti_json:
        checker = problem.get("checker_settings", {})

        time_limit_seconds = checker.get("limits", {}).get("time_limit_seconds")
        time_limit_millis = int(time_limit_seconds) * 1000 if time_limit_seconds is not None else None

        yandex_problem = {
            "problemMetadata": {
                "problemTypeMeta": problem.get("problem_type", None),
                "testFileType": None,
                "shortName": "",
                "defaultLocale": None,
                "names": problem.get("problem_name", {}),
                "statements": [{
                    "locale": None,
                    "type": "MARKDOWN",
                    "path": None,
                    "state": "VALID",
                    "rendered": True,
                    "texStatement": None,
                    "markdownStatement": {
                        "legend": problem.get("problem_description", ""),
                        "inputFormat": None,
                        "outputFormat": None,
                        "notes": None,
                        "showLimits": True
                    },
                    "renderingError": None
                }],
                "fileSet": {
                    "inputFile": problem.get("required_files", {}).get("input_file", None),
                    "outputFile": problem.get("required_files", {}).get("output_file", None),
                    "redirectStdin": problem.get("required_files", {}).get("redirect_stdin", None),
                    "redirectStdout": problem.get("required_files", {}).get("redirect_stdout", None)
                },
                "solutionLimits": {
                    "timeLimitMillis": int(problem.get("execution_constraints", {}).get("time_limit_seconds") * 1000) if problem.get("execution_constraints", {}).get("time_limit_seconds", None) is not None else None,
                    "idlenessLimitMillis": problem.get("execution_constraints", {}).get("idleness_limit_millis", None),
                    "memoryLimit": int(problem.get("execution_constraints", {}).get("memory_limit_mb")) if problem.get("execution_constraints", {}).get("memory_limit_mb", None) is not None else None,
                    "outputLimit": problem.get("execution_constraints", {}).get("output_limit", None)
                }
            },
            "testSets": [],
            "checkerSettings": {
                "checkerType": checker.get("checker_type", ""),
                "limits": {
                    "timeLimitMillis": time_limit_millis,
                    "idlenessLimitMillis": checker.get("limits", {}).get("idleness_limit_millis", None),
                    "memoryLimit": checker.get("limits", {}).get("memory_limit_mb", None),
                    "outputLimit": checker.get("limits", {}).get("output_limit", None)
                },
                "env": {},
                "checkerFiles": None,
                "isScoring": None,
                "checkerId": None,
                "eps": None,
                "absolute": None
            },
        }

        i = 0
        for test_set in problem.get("file_tests", []):
            matched_tests = []
            for test in test_set.get("tests", []):
                matched_tests.append({
                    "inputPath": test.get("input_path", None),
                    "answerPath": test.get("answer_path", None),
                    "inputExists": test.get("input_exists", False),
                    "answerExists": test.get("answer_exists", False)
                })
            yandex_problem["testSets"].append({
                "name": test_set.get("name", None),
                "inputFilePattern": test_set.get("input_file_pattern", None),
                "answerFilePattern": test_set.get("answer_file_pattern", None),
                "matchedTests": matched_tests
            })
            i += 1
        yandex_json["problems"].append(yandex_problem)

    return yandex_json

def convert_lti_to_yandex(uploaded_file):
    # lti_json = json.loads(uploaded_file.read())
    # yandex_json = convert_problem(lti_json)

    file_content = uploaded_file.read()
    lti_json = json.loads(file_content)
    yandex_json = convert_problem(lti_json)

    return yandex_json

def call_converter_to_yandex(uploaded_file):
    yandex_json = convert_lti_to_yandex(uploaded_file)
    return yandex_json
    #print(json.dumps(yandex_json, indent=4, ensure_ascii=False).encode('utf-8').decode())