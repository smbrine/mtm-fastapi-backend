import unittest
import os
from fastapi.testclient import TestClient
from app.main import app


class TestPhotoEndpoint(unittest.TestCase):
    def test_add_photo(self):
        # Initialize the test client
        client = TestClient(app)

        # Define the path to the test photo
        test_photo_path = "./tests/test_data/test_photo.png"

        # Ensure the test photo file exists
        self.assertTrue(
            os.path.isfile(test_photo_path), "Test photo file does not exist."
        )

        # Open the test photo file in binary mode
        with open(test_photo_path, "rb") as test_photo_file:
            # Prepare data to send
            data = {
                "query": (
                    None,
                    '{"description": "Test Description", '
                    '"latitude": 1.23, "longitude": 4.56, "record_id": "uuid-for-record", '
                    '"date_taken": "2024-01-07"}',
                    "application/json",
                ),
                "photo": ("test_photo.png", test_photo_file, "image/png"),
            }

            # Make the request
            response = client.post("/photo/add", files=data)

            # Check the response
            self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
