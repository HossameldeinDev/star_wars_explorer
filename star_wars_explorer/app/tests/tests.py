from unittest.mock import patch
from pathlib import Path

from django.test import TestCase

from .mocked_data import mocked_data_path
from ..models import Collection


class CollectionTests(TestCase):
    @patch("star_wars_explorer.app.utils.data_path", mocked_data_path)
    def setUp(self) -> None:
        Path(mocked_data_path).mkdir(parents=True, exist_ok=True)
        self.collection = Collection.objects.create(
            file_name="test.csv",
        )

    def test_string_representation(self):
        collection = Collection(file_name="test.csv")
        self.assertEqual(str(collection), collection.file_name)

    def test_content(self):
        self.assertEqual(f"{self.collection.file_name}", "test.csv")

