import sys
import unittest
from pathlib import Path
import os
import main
import solution
import inspect
from typing import List, Dict
from dataclasses import dataclass
import io
import contextlib

project_name = Path(os.path.abspath(__file__)).parent.parent.parent.name
cwd = Path.cwd()
parts = cwd.parts
basefolder_index = parts.index(project_name)
basepath = Path(*parts[: basefolder_index + 1])
sys.path.append(str(basepath))
from ttools.skyprotests.tests import SkyproTestCase, StdoutCapturing  # noqa: E402
from ttools.skyprotests.tests_mixins import AnnotationsCheckMixin  # noqa: E402


class DataClassesTestCase(SkyproTestCase, AnnotationsCheckMixin):

    def test_dataclasses_is_correct(self):
        expected_classes = ["University", "Occupation", "OnlineInfo", "User", "VkResponse", "VkData"]
        for cls in expected_classes:

            self.assertTrue(
                hasattr(main, cls),
                f"%@Проверьте, что класс {cls} определён в модуле"
            )

            inspected_class = getattr(main, cls)
            author_class = getattr(solution, cls)
            self.assertIn(
                "@dataclass", inspect.getsource(inspected_class),
                "%@Проверьте что используемые Вами классы являются датаклассами"
            )

            expected_fields = [x for x in author_class.__dataclass_fields__]
            student_fields = [x for x in inspected_class.__dataclass_fields__]

            for field in expected_fields:
                self.assertIn(
                    field, student_fields,
                    f"%@Проверьте, что класс {inspected_class.__name__} содержит поле {field}"
                )

        simple_type_classes = ["University", "Occupation", "OnlineInfo"]
        for cls in simple_type_classes:
            student_annotations = getattr(main, cls).__annotations__
            author_annotations = getattr(solution, cls).__annotations__

            for annotation in author_annotations:
                self.assertIn(
                    annotation, student_annotations,
                    f"%@Проверьте что написали аннотацию для аргумента {annotation}"
                )

            for annotation in author_annotations:
                self.assertEqual(
                    student_annotations.get(annotation), author_annotations.get(annotation),
                    f"%@Проверьте что правильно указали аннотацию для аргумента {annotation}"
                )

        university = main.University
        Occupation = main.Occupation
        onlineinfo = main.OnlineInfo

        @dataclass
        class User:
            id: int
            first_name: str
            last_name: str
            online_info: onlineinfo
            occupation: Dict[str, Occupation]
            universities: List[university]

        self.check_annotations(main.User, User)

        user = main.User

        @dataclass
        class VkResponse:
            count: int
            items: List[user]

        self.check_annotations(main.VkResponse, VkResponse)

        vkresponse = main.VkResponse

        @dataclass
        class VkData:
            response: vkresponse

        self.check_annotations(main.VkData, VkData)

        function_name = "get_vk_data"
        valid_json = solution.vk_data
        invalid_json = {}
        vkdata_class = main.VkData
        self.assertTrue(
            hasattr(main, function_name),
            "%@Проверьте что в модуле есть функция get_vk_data"
        )
        try:
            result = main.get_vk_data(valid_json)
        except:
            self.fail(f"%@Проверьте, что при вызове функции {function_name} с корректными данными не происходит ошибки")

        self.assertIsInstance(
            result, vkdata_class,
            f"%@Проверьте, что функция {function_name} возвращает экземпляр класса {vkdata_class.__name__}"
        )

        with self.assertRaises(
                ValueError,
                msg=f"%@Проверьте, что при вызове функции {function_name} с некорректными данными выбрасывается исключение ValueError"
        ):
            main.get_vk_data(invalid_json)

        cwd = os.getcwd()
        path = Path(cwd)
        path = path.joinpath("main.py")
        stream = os.popen(f'mypy {path}')
        output = stream.read()
        self.assertIn(
            "Success", output,
            "%@Попробуйте проверить свою задачу с помощью утилиты mypy, скорее всего там еще остались ошибки"
            "Возможно где-то отсутствует аннтотация, или в функцию передан аргумент неверного типа"
        )


if __name__ == "__main__":
    unittest.main()
