import os
import re
import shutil
from os.path import isfile
from unittest.mock import patch
from pathlib import Path

import petl
from django.test import TestCase
from django.urls import reverse

from .mocked_data import mocked_planets, mocked_people, mocked_data_path
from ..models import Collection


class CollectionTests(TestCase):
    @patch("star_wars_explorer.app.utils.data_path", mocked_data_path)
    def setUp(self) -> None:
        Path(mocked_data_path).mkdir(parents=True, exist_ok=True)
        self.collection = Collection.objects.create(
            file_name="test.csv",
        )

    @patch("star_wars_explorer.app.utils.data_path", mocked_data_path)
    def tearDown(self) -> None:
        from ..utils import data_path

        shutil.rmtree(data_path)
        os.mkdir(data_path)

    def test_string_representation(self):
        collection = Collection(file_name="test.csv")
        self.assertEqual(str(collection), collection.file_name)

    def test_content(self):
        self.assertEqual(f"{self.collection.file_name}", "test.csv")

    def test_collection_list_view(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home.html")
        self.assertTrue("collection_list" in response.context)
        self.assertEqual(response.context["collection_list"].first(), self.collection)

    @patch("star_wars_explorer.app.views.data_path", mocked_data_path)
    @patch("star_wars_explorer.app.utils.data_path", mocked_data_path)
    @patch("star_wars_explorer.app.utils.crawl_planets", return_value=mocked_planets)
    @patch("star_wars_explorer.app.utils.crawl_people", return_value=mocked_people)
    def test_crawl_function(self, _, __):
        from star_wars_explorer.app.utils import crawl, data_path

        collection = crawl()
        self.assertTrue(isinstance(collection, Collection))
        self.assertTrue(hasattr(collection, "file_name"))
        self.assertTrue(hasattr(collection, "date"))
        file_path = data_path / collection.file_name
        self.assertTrue(isfile(file_path))
        data = petl.fromcsv(file_path)
        self.assertEqual(petl.values(data, "name")[0], mocked_people[0]["name"])

    @patch("star_wars_explorer.app.views.data_path", mocked_data_path)
    @patch("star_wars_explorer.app.utils.data_path", mocked_data_path)
    @patch("star_wars_explorer.app.utils.crawl_planets", return_value=mocked_planets)
    @patch("star_wars_explorer.app.utils.crawl_people", return_value=mocked_people)
    def test_collection_detail_view(self, _, __):
        from star_wars_explorer.app.utils import crawl, data_path

        collection = crawl()
        response = self.client.get(f"/collection/{collection.id}/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "collection_detail.html")
        self.assertContains(response, "Test Hair color")
        file_path = data_path / collection.file_name
        self.assertTrue(isfile(file_path))

    @patch("star_wars_explorer.app.views.data_path", mocked_data_path)
    @patch("star_wars_explorer.app.utils.data_path", mocked_data_path)
    @patch("star_wars_explorer.app.utils.crawl_planets", return_value=mocked_planets)
    @patch("star_wars_explorer.app.utils.crawl_people", return_value=mocked_people)
    def test_get_collection_view(self, _, __):
        from star_wars_explorer.app.utils import data_path

        response = self.client.get("/collection/fetcher")
        self.assertEqual(response.status_code, 302)
        collection_id = re.findall(r"collection/(\d+)", response.url)[0]
        collection = Collection.objects.get(pk=collection_id)
        file_path = data_path / collection.file_name
        self.assertTrue(isfile(file_path))

