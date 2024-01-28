from scripts.YandexToLTI import call_converter_from_yandex
from scripts.StepikToLTI import call_converter_from_stepic
import sys

if __name__ == '__main__':
    try:
        # call_converter_from_yandex()
        call_converter_from_stepic()
    except AttributeError as er:
        print("Невозможно обработать файл из-за отсутствия какого-то из атрибутов, ", er)
    except:
        print("При обработке файла произошла ошибка, ", sys.exc_info())


