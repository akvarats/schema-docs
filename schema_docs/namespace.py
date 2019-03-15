from schema_docs.i import ISchemaDocNamespace


class SchemaDocNamespace(ISchemaDocNamespace):

    def __init__(self):
        self._types = {}

    @property
    def types(self) -> dict:
        return self._types

    def __getattr__(self, item):
        return self.types[item]
