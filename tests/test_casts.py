import unittest

from schema_docs import build_schemadoc_namespace
from schema_docs.exceptions import SchemaDocFieldException


class TestCasts(unittest.TestCase):

    def test_soft_numbers(self):
        schema = [{
            "name": "Document1",
            "options": {"soft_numbers": True},
            "fields": {
                "x": "number"
            }
        }, {
            "name": "Document2",
            "fields": {
                "y": "num"
            }
        }]

        ns = build_schemadoc_namespace(schema)

        doc1 = ns.Document1()
        doc2 = ns.Document2().setup(soft_numbers=True)

        doc1.x = "11"
        doc2.y = "22"

        self.assertEqual(doc1.x + doc2.y, 33)

    def test_try_invalid_for_soft_number(self):

        schema = [{
            "name": "Document",
            "fields": {
                "x": "number"
            }
        }]

        doc = build_schemadoc_namespace(schema).Document().setup(soft_numbers=True)

        try:
            doc.x = "abc"
            self.fail("Удалось записать невалидное для soft_number значение")
        except SchemaDocFieldException as e:
            # всё ок, должно прийти такое сообщение
            pass

    def test_non_soft_numbers(self):

        schema = [{
            "name": "Document",
            "fields": {
                "x": "number"
            }
        }]

        doc = build_schemadoc_namespace(schema).Document()

        try:
            doc.x = "10"
            self.fail("Строка ошибочно принята как число")
        except SchemaDocFieldException as e:
            # всё ок, должно прийти такое сообщение
            pass
