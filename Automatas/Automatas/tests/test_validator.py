import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from validator import validate, extract_valid_name


class ValidatorTests(unittest.TestCase):
    def test_valid_present_affirmative(self):
        self.assertTrue(validate("I am a teacher").valid)
        self.assertEqual(validate("The cat is brown.").category, "present affirmative")

    def test_valid_age_expressions(self):
        self.assertEqual(validate("He is 24 years old").category, "present affirmative")
        self.assertEqual(validate("I am 10 years old").category, "present affirmative")
        self.assertEqual(validate("She is 1 year old").category, "present affirmative")

    def test_invalid_present_negative(self):
        self.assertFalse(validate("She is not a nice girl").valid)

    def test_invalid_past_forms(self):
        self.assertFalse(validate("You were a good student").valid)
        self.assertFalse(validate("Maria was not sick last week").valid)

    def test_invalid_questions(self):
        self.assertFalse(validate("Are the boys happy?").valid)
        self.assertFalse(validate("Was the dog furious?").valid)

    def test_invalid_agreement(self):
        result = validate("I is student")
        self.assertFalse(result.valid)
        self.assertIn("agreement", result.message.lower())

    def test_invalid_without_to_be(self):
        result = validate("She likes music")
        self.assertFalse(result.valid)
        self.assertIn("to be", result.message.lower())

    def test_invalid_word_order(self):
        result = validate("Is she a nice girl")
        self.assertFalse(result.valid)

    def test_spanish_sentences(self):
        result = validate("esta lloviendo en cartagena")
        self.assertFalse(result.valid)
        self.assertIn("spanish", result.message.lower())

        result2 = validate("Carlos is estudiante")
        self.assertFalse(result2.valid)
        self.assertIn("spanish", result2.message.lower())

        result3 = validate("Yo soy profesor")
        self.assertFalse(result3.valid)
        self.assertIn("spanish", result3.message.lower())

    def test_extract_valid_name(self):
        self.assertEqual(extract_valid_name("Carlos"), "Carlos")
        self.assertEqual(extract_valid_name("carlos"), "Carlos")
        self.assertEqual(extract_valid_name("My name is Carlos"), "Carlos")
        self.assertEqual(extract_valid_name("I am Carlos"), "Carlos")
        self.assertEqual(extract_valid_name("Maria Jose"), "Maria Jose")

        # Invalid names
        self.assertIsNone(extract_valid_name("He is 24 years old"))
        self.assertIsNone(extract_valid_name("She is happy"))
        self.assertIsNone(extract_valid_name("123"))
        self.assertIsNone(extract_valid_name("hello"))
        self.assertIsNone(extract_valid_name("I am a student"))


if __name__ == "__main__":
    unittest.main()
