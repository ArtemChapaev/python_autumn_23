import unittest
from unittest import mock

from json_parser import parse_json


class MyParseJson(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_simple_case(self):
        json_str = '{"key1": "Word1 word2", "key2": "word2 word3"}'
        keywords = ["key1"]
        required_fields = ["word2"]

        mock_callback = mock.Mock(return_value=None)
        parse_json(json_str, keywords, required_fields, mock_callback)

        mock_callback.assert_called_once_with("word2")

    def test_case_insensitivity(self):
        json_str = '{"key1": "Word1 word2", "key2": "word2 word3"}'
        keywords = ["key1"]
        required_fields = ["word1"]

        mock_callback = mock.Mock(return_value=None)
        parse_json(json_str, keywords, required_fields, mock_callback)

        mock_callback.assert_called_once_with("word1")

    def test_multiple_callback_calls(self):
        json_str = '{"key1": "Word1 word2", "key2": "word2 word3"}'
        keywords = ["key1", "key2"]
        required_fields = ["word1", "word3"]

        mock_callback = mock.Mock(return_value=None)
        parse_json(json_str, keywords, required_fields, mock_callback)

        expected_calls = [
            mock.call("word1"),
            mock.call("word3")
        ]
        self.assertEqual(expected_calls, mock_callback.mock_calls)

    def test_not_called_callback(self):
        json_str = '{"key1": "Word1 word2", "key2": "word2 word3"}'
        keywords = ["key1"]
        required_fields = ["word3"]

        mock_callback = mock.Mock(return_value=None)
        parse_json(json_str, keywords, required_fields, mock_callback)

        mock_callback.assert_not_called()

    def test_multiple_uses_with_error_types(self):
        with self.assertRaises(TypeError):
            parse_json(123, [], [], mock.Mock())

        with self.assertRaises(TypeError):
            parse_json("{}", "not_a_list", [], mock.Mock())

        with self.assertRaises(TypeError):
            parse_json("{}", [], "not_a_list", mock.Mock())

    def test_empty_json_str(self):
        json_str = ""
        keywords = []
        required_fields = []

        mock_callback = mock.Mock(return_value=None)
        parse_json(json_str, keywords, required_fields, mock_callback)
        mock_callback.assert_not_called()


if __name__ == '__main__':
    unittest.main()
