import unittest

from schema_docs.api import build_schemadoc_namespace

class TestsValidation(unittest.TestCase):
    """
    Validation tests
    """

    def test_string_field_validation(self):

        schema = [{
            'name': 'Document',
            'fields': {
                'name': {'type': 'string', 'validate': 'required'},
                'code': {'type': 'string', 'validate': 'not-empty'},
            }
        }]

        ns = build_schemadoc_namespace(schema)

        doc = ns.Document()

        self.assertFalse(doc.validate())
        self.assertEqual(len(doc.failed_validations()), 2)

        doc.name = ''
        self.assertFalse(doc.validate())
        self.assertEqual(len(doc.failed_validations()), 1)

        doc.code = ''
        self.assertFalse(doc.validate())
        self.assertEqual(len(doc.failed_validations()), 1)

        doc.code = '1'
        self.assertTrue(doc.validate())