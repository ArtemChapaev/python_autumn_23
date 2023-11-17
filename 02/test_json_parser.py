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
        required_fields = ["key1"]
        keywords = ["word2"]

        mock_callback = mock.Mock(return_value=None)
        parse_json(json_str, required_fields, keywords, mock_callback)

        mock_callback.assert_called_once_with("key1", "word2")

    def test_case_insensitivity(self):
        json_str = '{"key1": "Word1 word2", "key2": "word2 word3"}'
        required_fields = ["key1"]

        keywords = ["word1"]
        mock_callback = mock.Mock(return_value=None)

        parse_json(json_str, required_fields, keywords, mock_callback)
        mock_callback.assert_called_once_with("key1", "word1")

        keywords = ["Word2"]
        mock_callback = mock.Mock(return_value=None)

        parse_json(json_str, required_fields, keywords, mock_callback)
        mock_callback.assert_called_once_with("key1", "word2")

    def test_multiple_callback_calls(self):
        json_str = '{"key1": "Word1 word2", "key2": "word2 word3"}'

        required_fields = ["key1", "key2"]
        keywords = ["word1", "word3"]
        mock_callback = mock.Mock(return_value=None)

        parse_json(json_str, required_fields, keywords, mock_callback)
        expected_calls = [
            mock.call("key1", "word1"),
            mock.call("key2", "word3")
        ]
        self.assertEqual(expected_calls, mock_callback.mock_calls)

        required_fields = ["key1", "key2"]
        keywords = ["word2"]

        mock_callback = mock.Mock(return_value=None)
        parse_json(json_str, required_fields, keywords, mock_callback)
        expected_calls = [
            mock.call("key1", "word2"),
            mock.call("key2", "word2")
        ]
        self.assertEqual(expected_calls, mock_callback.mock_calls)

        json_str = '{"key1": "Word1 word3"}'
        required_fields = ["key1"]
        keywords = ["word1", "word3"]
        mock_callback = mock.Mock(return_value=None)

        parse_json(json_str, required_fields, keywords, mock_callback)
        expected_calls = [
            mock.call("key1", "word1"),
            mock.call("key1", "word3")
        ]
        self.assertEqual(expected_calls, mock_callback.mock_calls)

    def test_not_called_callback(self):
        json_str = '{"key1": "Word1 word2", "key2": "word2 word3"}'

        required_fields = ["key1"]
        keywords = ["word3"]
        mock_callback = mock.Mock(return_value=None)

        parse_json(json_str, required_fields, keywords, mock_callback)
        mock_callback.assert_not_called()

        required_fields = ["key1"]
        keywords = ["word4"]
        mock_callback = mock.Mock(return_value=None)

        parse_json(json_str, required_fields, keywords, mock_callback)
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
        required_fields = []
        keywords = []

        mock_callback = mock.Mock(return_value=None)

        parse_json(json_str, required_fields, keywords, mock_callback)
        mock_callback.assert_not_called()


if __name__ == '__main__':
    unittest.main()
