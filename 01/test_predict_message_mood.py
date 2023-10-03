import unittest
from unittest import mock

from predict_message_mood import SomeModel, predict_message_mood


class TestPredictMessageModel(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_several_values_simple(self):
        model = SomeModel()
        with mock.patch("predict_message_mood.SomeModel.predict") as mock_fetch:
            mock_fetch.side_effect = [0.1, 0.4, 0.9]

            self.assertEqual("неуд", predict_message_mood("к", model))
            self.assertEqual("норм", predict_message_mood("код ", model))
            self.assertEqual("отл", predict_message_mood("код код к", model))

            expected_calls = [
                mock.call("к"),
                mock.call("код "),
                mock.call("код код к")
            ]
            self.assertEqual(expected_calls, mock_fetch.mock_calls)

    def test_all_default_thresholds_values(self):
        model = SomeModel()
        with mock.patch("predict_message_mood.SomeModel.predict") as mock_fetch:
            mock_fetch.side_effect = [0.0, 0.3, 0.8, 1]

            self.assertEqual("неуд", predict_message_mood("", model))
            self.assertEqual("норм", predict_message_mood("код", model))
            self.assertEqual("норм", predict_message_mood("код код ", model))
            self.assertEqual("отл", predict_message_mood("код код ко", model))

            expected_calls = [
                mock.call(""),
                mock.call("код"),
                mock.call("код код "),
                mock.call("код код ко")
            ]
            self.assertEqual(expected_calls, mock_fetch.mock_calls)

    def test_several_values_with_custom_bad_thresholds(self):
        model = SomeModel()
        with mock.patch("predict_message_mood.SomeModel.predict") as mock_fetch:
            mock_fetch.side_effect = [0.3, 0.3]

            self.assertEqual("неуд", predict_message_mood("код", model, bad_thresholds=0.4))
            self.assertEqual("норм", predict_message_mood("код", model, bad_thresholds=0.2))

            expected_calls = [
                mock.call("код"),
                mock.call("код")
            ]
            self.assertEqual(expected_calls, mock_fetch.mock_calls)

    def test_several_values_with_custom_good_thresholds(self):
        model = SomeModel()
        with mock.patch("predict_message_mood.SomeModel.predict") as mock_fetch:
            mock_fetch.side_effect = [0.8, 0.7]

            self.assertEqual("норм", predict_message_mood("код код ", model, good_thresholds=0.9))
            self.assertEqual("отл", predict_message_mood("код код", model, good_thresholds=0.6))

            expected_calls = [
                mock.call("код код "),
                mock.call("код код")
            ]
            self.assertEqual(expected_calls, mock_fetch.mock_calls)

    def test_several_values_with_error_thresholds(self):
        model = SomeModel()
        with mock.patch("predict_message_mood.SomeModel.predict") as mock_fetch:
            mock_fetch.side_effect = [0.3 for _ in range(6)]

            with self.assertRaises(ValueError) as err:
                predict_message_mood("код", model, good_thresholds=-0.1)
                self.assertEqual(ValueError, type(err.exception))

            with self.assertRaises(ValueError) as err:
                predict_message_mood("код", model, good_thresholds=1.1)
                self.assertEqual(ValueError, type(err.exception))

            with self.assertRaises(ValueError) as err:
                predict_message_mood("код", model, bad_thresholds=-0.1)
                self.assertEqual(ValueError, type(err.exception))

            with self.assertRaises(ValueError) as err:
                predict_message_mood("код", model, bad_thresholds=1.1)
                self.assertEqual(ValueError, type(err.exception))

            with self.assertRaises(ValueError) as err:
                predict_message_mood("код", model, bad_thresholds=1.1, good_thresholds=1.1)
                self.assertEqual(ValueError, type(err.exception))

            with self.assertRaises(ValueError) as err:
                predict_message_mood("код", model, bad_thresholds=-0.1, good_thresholds=-0.1)
                self.assertEqual(ValueError, type(err.exception))

            with self.assertRaises(ValueError) as err:
                predict_message_mood("код", model, bad_thresholds=0.8, good_thresholds=0.1)
                self.assertEqual(ValueError, type(err.exception))

            expected_calls = []
            self.assertEqual(expected_calls, mock_fetch.mock_calls)

    def test_several_values_with_error_types(self):
        model = SomeModel()
        with mock.patch("predict_message_mood.SomeModel.predict") as mock_fetch:
            mock_fetch.side_effect = [0.3 for _ in range(4)]

            with self.assertRaises(TypeError) as err:
                predict_message_mood(88005353535, model)
                self.assertEqual(TypeError, type(err.exception))

            with self.assertRaises(TypeError) as err:
                predict_message_mood("код", "код")
                self.assertEqual(TypeError, type(err.exception))

            with self.assertRaises(TypeError) as err:
                predict_message_mood("код", model, bad_thresholds="bad")
                self.assertEqual(TypeError, type(err.exception))

            with self.assertRaises(TypeError) as err:
                predict_message_mood("код", model, good_thresholds="good")
                self.assertEqual(TypeError, type(err.exception))

            expected_calls = []
            self.assertEqual(expected_calls, mock_fetch.mock_calls)


if __name__ == "__main__":
    unittest.main()
