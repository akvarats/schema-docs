from schema_docs.builder import SchemaDocBuilder
from schema_docs.i import ISchemaDocNamespace


def build_schemadoc_namespace(schema) -> ISchemaDocNamespace:
    """ """
    return SchemaDocBuilder().build_namespace(schema)
