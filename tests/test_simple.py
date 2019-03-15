import unittest
import datetime

from schema_docs import build_schemadoc_namespace
from schema_docs.utils import date_to_iso


class SimpleTests(unittest.TestCase):

    def test_creation(self):
        schema = [{
            'name': 'Document',
            'fields': {
                'date': 'date'
            }
        }]

        today = datetime.date.today()

        ns = build_schemadoc_namespace(schema)
        doc = ns.Document(date=today)

        self.assertEqual(doc.to_dict()['date'], date_to_iso(today))

