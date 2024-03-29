from scripts.LTIToStepik import convert_problem as convert_to_step
from scripts.LTIToYandex import convert_problem as convert_to_yandex
from scripts.LTIToLMS import convert_problem as convert_to_lms
from scripts.YandexToLTI import call_converter_from_yandex
from scripts.StepikToLTI import call_converter_from_stepic
from scripts.LMSToLTI import call_converter_from_lms
import tempfile
import os
import json

def convert_yandex_to_stepik(uploaded_file):
    lti_json = call_converter_from_yandex(uploaded_file)
    stepik_json = convert_to_step(lti_json)
    return stepik_json


def convert_yandex_to_smartlms(uploaded_file):
    lti_result = call_converter_from_yandex(uploaded_file)
    smartlms_result = convert_to_lms(lti_result)
    return smartlms_result

def convert_stepik_to_yandex(uploaded_file):
    lti_result = call_converter_from_stepic(uploaded_file)
    yandex_result = convert_to_yandex(lti_result)
    return yandex_result

def convert_stepik_to_smartlms(uploaded_file):
    lti_result = call_converter_from_stepic(uploaded_file)
    smartlms_result = convert_to_lms(lti_result)
    return smartlms_result

def convert_smartlms_to_yandex(uploaded_file):
    lti_result = call_converter_from_lms(uploaded_file)
    yandex_result = convert_to_yandex(lti_result)
    return yandex_result

def convert_smartlms_to_stepik(uploaded_file):
    lti_result = call_converter_from_lms(uploaded_file)
    stepik_result = convert_to_step(lti_result)
    return stepik_result
