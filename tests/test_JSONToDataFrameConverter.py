import sys
sys.path.append('/Users/sid/projects/psi/new-ecopylot/EcoPyLot')
import json
import unittest
from EcoPyLot.JSONToDataFrameConverter import JSONToDataFrameConverter

class TestJSONToDataFrameConverter(unittest.TestCase):
    def setUp(self):
        # JSON input for testing
        self.test_json = """
        {
            "test_uid": {
                "parameter": "seats",
                "year": 2000,
                "fuselage": "TW",
                "energy source": "H2",
                "energy conversion": "FC",
                "Transmission": "Elec",
                "Propulsor": "Prop",
                "Drag Reduction": "None",
                "sizes": ["Commuter", "Regional"],
                "amount": 75,
                "loc": 75,
                "minimum": 50,
                "maximum": 100,
                "kind": "distribution",
                "uncertainty_type": 5,
                "source": "Test Source",
                "url": "https://example.com",
                "comment": "Test comment"
            }
        }
        """
        self.converter = JSONToDataFrameConverter(self.test_json)

    def test_dataframe_shape(self):
        df = self.converter.create_dataframe()
        self.assertEqual(df.shape, (2, 19))  # 2 rows, 16 columns

    def test_dataframe_content(self):
        df = self.converter.create_dataframe()
        # Check if the dataframe contains correct data for a specific column
        self.assertIn("Commuter", df['sizes'].values)
        self.assertIn("Regional", df['sizes'].values)

    def test_invalid_json(self):
        with self.assertRaises(json.JSONDecodeError):
            JSONToDataFrameConverter("invalid json")

# This allows the test to be run from the command line
if __name__ == '__main__':
    unittest.main()
