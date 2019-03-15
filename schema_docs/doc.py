from schema_docs.exceptions import InvalidSchemaDocException
from .i import ISchemaDoc
from .caster import SchemaDocCaster
from .validation import SchemaDocValidator

class SchemaDoc(ISchemaDoc):
    """ Документ """

    def __init__(self, *args, **options):
        self._cast = SchemaDocCaster()
        self._validator = SchemaDocValidator()
        self._data = dict()

        if args and isinstance(args[0], dict):
            self.from_dict(args[0])

        for field_name in self.schema['fields'].keys():
            if field_name in options:
                setattr(self, field_name, options[field_name])

    def __getattr__(self, item):
        """ """
        if item in self.schema['fields']:
            return self._cast.to_ext(
                value=self._data.get(item),
                field_name=item,
                field_def=self.schema['fields'][item],
                doc=self
            )

        raise AttributeError('Attribute "{0}" is not defined'.format(item))

    def __setattr__(self, key, value):
        """ """
        if key in self.schema['fields']:
            self._data[key] = self._cast.from_ext(
                value=value,
                field_name=key,
                field_def=self.schema['fields'][key],
                doc=self
            )
        else:
            super(SchemaDoc, self).__setattr__(key, value)

    def to_dict(self) -> dict:
        return self._data

    def from_dict(self, value):
        self._data = value
        return self

    def __str__(self):
        return '{0}: {1}'.format(self.schema['name'], self.to_dict())

    def failed_validations(self):
        return self._validator.failed_validation(schema_doc=self)

    def validate(self, raise_exception=False):
        """
        Валидация документа

        :param raise_exception: если True, то при наличии невалидных значений выбрасывается исключение
        :return:
        """
        failed_validations = self.failed_validations()

        if failed_validations and raise_exception:
            raise InvalidSchemaDocException(failed_validations=failed_validations)

        return not failed_validations
