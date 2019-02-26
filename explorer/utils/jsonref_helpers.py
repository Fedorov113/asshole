import jsonref
from jsonschema import validate
from os.path import join, dirname


def assert_valid_schema(data, schema_file):
    """ Checks whether the given data matches the schema """

    schema = _load_json_schema(schema_file)
    return validate(data, schema)


def _load_json_schema(filename):
    """ Loads the given schema file """

    relative_path = join('schemas', filename)
    print(relative_path)
    absolute_path = join(dirname(__file__), relative_path)
    print(absolute_path)

    base_path = dirname(absolute_path)
    base_uri = 'file://{}/'.format(base_path)
    print(base_uri)

    with open(absolute_path) as schema_file:
        return jsonref.loads(schema_file.read(), base_uri=base_uri, jsonschema=True)