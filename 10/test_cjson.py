import unittest
import json

import cjson


class TestCjson(unittest.TestCase):
    def test_cjson_dumps_loads(self):
        example_dict = {"name": "Artem"}
        cjson_loaded_dict = cjson.loads(cjson.dumps(example_dict))
        self.assertEqual(example_dict, cjson_loaded_dict)

        example_dict = {"age": 19}
        cjson_loaded_dict = cjson.loads(cjson.dumps(example_dict))
        self.assertEqual(example_dict, cjson_loaded_dict)

        example_dict = {"name": "Artem", "age": 19}
        cjson_loaded_dict = cjson.loads(cjson.dumps(example_dict))
        self.assertEqual(example_dict, cjson_loaded_dict)


class TestJsonLoads(unittest.TestCase):
    def test_cjson_usual_loads(self):
        example_str = '{"name": "Artem"}'
        json_dict = json.loads(example_str)
        cjson_dict = cjson.loads(example_str)
        self.assertEqual(json_dict, cjson_dict)

        example_str = '{"age": 19}'
        json_dict = json.loads(example_str)
        cjson_dict = cjson.loads(example_str)
        self.assertEqual(json_dict, cjson_dict)

        example_str = '{"name": "Artem", "age": 19}'
        json_dict = json.loads(example_str)
        cjson_dict = cjson.loads(example_str)
        self.assertEqual(json_dict, cjson_dict)

        example_str = "{\"name\": \"Artem\", \"age\": 19}"
        json_dict = json.loads(example_str)
        cjson_dict = cjson.loads(example_str)
        self.assertEqual(json_dict, cjson_dict)

    def test_cjson_loads_str_immutability(self):
        example_str = '{"name": "Artem", "age": 19}'
        cjson.loads(example_str)
        self.assertEqual('{"name": "Artem", "age": 19}', example_str)

    def test_cjson_loads_error_types(self):
        example_num = 6
        with self.assertRaises(TypeError) as err:
            cjson.loads(example_num)
        self.assertEqual(type(err.exception), TypeError)

        example_dict = {"credentials": ["login", "password"], "name": "Artem", "age": 19}
        with self.assertRaises(TypeError) as err:
            cjson.loads(example_dict)
        self.assertEqual(type(err.exception), TypeError)

    def test_cjson_loads_error_key_types(self):
        example_str = '{"credentials": ["login", "password"], "name": "Artem", "age": 19}'
        with self.assertRaises(TypeError) as err:
            cjson.loads(example_str)
        self.assertEqual(type(err.exception), TypeError)

        example_str = '{"name": "Artem", "credentials": ["login", "password"], "age": 19}'
        with self.assertRaises(TypeError) as err:
            cjson.loads(example_str)
        self.assertEqual(type(err.exception), TypeError)

        example_str = '\'name\': "Artem", "age": 19}'
        with self.assertRaises(TypeError) as err:
            cjson.loads(example_str)
        self.assertEqual(type(err.exception), TypeError)

    def test_cjson_loads_error_value_types(self):
        example_str = '{10: "Artem", "age": 19}'
        with self.assertRaises(TypeError) as err:
            cjson.loads(example_str)
        self.assertEqual(type(err.exception), TypeError)

        example_str = '{"name": "Artem", 10: 19}'
        with self.assertRaises(TypeError) as err:
            cjson.loads(example_str)
        self.assertEqual(type(err.exception), TypeError)

        example_str = '"name": \'Artem\', "age": 19}'
        with self.assertRaises(TypeError) as err:
            cjson.loads(example_str)
        self.assertEqual(type(err.exception), TypeError)


class TestCjsonDumps(unittest.TestCase):
    def test_cjson_usual_dumps(self):
        example_dict = {"name": "Artem"}
        json_str = json.dumps(example_dict)
        cjson_str = cjson.dumps(example_dict)
        self.assertEqual(json_str, cjson_str)

        example_dict = {"age": 19}
        json_str = json.dumps(example_dict)
        cjson_str = cjson.dumps(example_dict)
        self.assertEqual(json_str, cjson_str)

        example_dict = {"name": "Artem", "age": 19}
        json_str = json.dumps(example_dict)
        cjson_str = cjson.dumps(example_dict)
        self.assertEqual(json_str, cjson_str)

    def test_cjson_dumps_dict_immutability(self):
        example_dict = {"name": "Artem", "age": 19}
        cjson.dumps(example_dict)
        self.assertEqual({"name": "Artem", "age": 19}, example_dict)

    def test_cjson_dumps_error_types(self):
        example_num = 6
        with self.assertRaises(TypeError) as err:
            cjson.dumps(example_num)
        self.assertEqual(type(err.exception), TypeError)

        example_str = '{"credentials": ["login", "password"], "name": "Artem", "age": 19}'
        with self.assertRaises(TypeError) as err:
            cjson.dumps(example_str)
        self.assertEqual(type(err.exception), TypeError)

    def test_cjson_dumps_error_key_types(self):
        example_dict = {"credentials": ["login", "password"], "name": "Artem", "age": 19}
        with self.assertRaises(TypeError) as err:
            cjson.dumps(example_dict)
        self.assertEqual(type(err.exception), TypeError)

        example_dict = {"name": "Artem", "credentials": ["login", "password"], "age": 19}
        with self.assertRaises(TypeError) as err:
            cjson.dumps(example_dict)
        self.assertEqual(type(err.exception), TypeError)

    def test_cjson_dumps_error_value_types(self):
        example_dict = {10: "Artem", "age": 19}
        with self.assertRaises(TypeError) as err:
            cjson.dumps(example_dict)
        self.assertEqual(type(err.exception), TypeError)

        example_dict = {"name": "Artem", 10: 19}
        with self.assertRaises(TypeError) as err:
            cjson.dumps(example_dict)
        self.assertEqual(type(err.exception), TypeError)


if __name__ == "__main__":
    unittest.main()
