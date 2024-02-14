import json

# Убедитесь, что в переданном файле сожержится только одна задача,
# в противном случае будет спаршена только первая задача из списка
def convert_problem(lti_json):
    stepik_json = {
        "block": {
            "name": "",
            "text": "",
            "video": None,
            "options": {
                "execution_time_limit": None,
                "execution_memory_limit": None,
                "limits": {},
                "code_templates": {},
                "code_templates_header_lines_count": {},
                "code_templates_footer_lines_count": {},
                "code_templates_options": {},
                "samples": [],
                "is_run_user_code_allowed": True
            },
            "subtitle_files": [],
            "is_deprecated": False,
            "source": {
                "code": "",
                "execution_time_limit": None,
                "execution_memory_limit": None,
                "samples_count": None,
                "templates_data": "",
                "is_time_limit_scaled": True,
                "is_memory_limit_scaled": True,
                "is_run_user_code_allowed": True,
                "manual_time_limits": [],
                "manual_memory_limits": [],
                "test_archive": [],
                "test_cases": []
            },
            "subtitles": {},
            "tests_archive": "",
            "feedback_correct": "",
            "feedback_wrong": ""
        },
        "id": "",
        "has_review": False,
        "time": None
    }

    problems = lti_json.get("problems", [])
    if not problems:
        return stepik_json

    problem = problems[0]

    problem_name = problem.get("problem_name", {})
    if problem_name:
        problem_name_en = problem_name.get("en")
        if problem_name_en:
            stepik_json["block"]["name"] = problem_name_en
        else:
            for value in problem_name.values():
                stepik_json["block"]["name"] = value

    stepik_json["block"]["text"] = problem.get("problem_description", "")
    stepik_json["block"]["source"]["code"] = problem.get("code_for_testing", "")

    execution_constraints = problem.get("execution_constraints", {})
    stepik_json["block"]["options"]["execution_time_limit"] = execution_constraints.get("time_limit_seconds", None)
    stepik_json["block"]["options"]["execution_memory_limit"] = execution_constraints.get("memory_limit_mb", None)

    private_constraints = execution_constraints.get("private_constraints", {})
    for lang, lang_limits in private_constraints.items():
        stepik_json["block"]["options"]["limits"][lang] = {
            "time": lang_limits.get("time_limit_seconds", None),
            "memory": lang_limits.get("memory_limit_mb", None)
        }

    templates = problem.get("code_template", {})
    templates_data = ""
    for lang, lang_templ in templates.items():
        stepik_json["block"]["options"]["code_templates"][lang] = lang_templ
        templates_data += f"::{lang}\n{lang_templ}"
    stepik_json["block"]["source"]["templates_data"] = templates_data

    stepik_json["block"]["source"]["test_cases"] = problem.get("test_cases", [])
    stepik_json["block"]["source"]["execution_time_limit"] = execution_constraints.get("time_limit_seconds", None)
    stepik_json["block"]["source"]["execution_memory_limit"] = execution_constraints.get("memory_limit_mb", None)

    stepik_json["id"] = problem.get("id", "")

    return stepik_json

def convert_lti_to_stepik(path):
    with open(path, 'r', encoding='utf-8') as file:
        lti_json = json.load(file)

    yandex_json = convert_problem(lti_json)
    return yandex_json

def call_converter_to_stepik():
    stepik_json = convert_lti_to_stepik('/Users/manankova15/Desktop/курсач/step_to_lti.json')
    print(json.dumps(stepik_json, indent=4, ensure_ascii=False).encode('utf-8').decode())