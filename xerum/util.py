from cerberus import Validator


class ValidationError(Exception):
    """This custom error class simply includes a message and the list of
    validation errors

    """
    def __init__(self, message, errors=None):
        super().__init__(message)
        self.errors = errors


def validate(document, schema):
    """Given a document and a schema, instantiate a Validator object
    (Cerberus) and try to validate the document

    """
    v = Validator(schema)
    if not v(document):
        raise ValidationError("Validation error", v.errors)
