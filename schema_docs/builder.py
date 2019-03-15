from .i import ISchemaDocBuilder, ISchemaDocNamespace
from .doc import SchemaDoc
from .namespace import SchemaDocNamespace


class SchemaDocBuilder(ISchemaDocBuilder):
    """
    Билдер для объектов
    """
    def build_namespace(self, schema) -> ISchemaDocNamespace:
        """
        Строит объекты по указанной схеме
        """
        schema = [schema] if isinstance(schema, dict) else schema

        ns = SchemaDocNamespace()

        for type_schema in schema:
            type_name = type_schema['name']
            ns.types[type_name] = type(type_name, (SchemaDoc, ), {'ns': ns, 'schema': type_schema})

        return ns
