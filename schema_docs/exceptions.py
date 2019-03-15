from typing import Optional


class SchemaDocFieldException(Exception):

    def __init__(self, msg, field_name, field_type, failed_value):
        self.msg = msg
        self.field_name = field_name
        self.field_type = field_type
        self.failed_value = failed_value

        super(SchemaDocFieldException, self).__init__(msg)


class InvalidSchemaDocException(Exception):
    """
    Исключение о том, что schema_doc не является валидным
    """
    def __init__(self, failed_validations=None):
        msg = '; '.join([fv.msg for fv in failed_validations])
        super(InvalidSchemaDocException, self).__init__(msg)
