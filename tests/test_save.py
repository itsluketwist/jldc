from dataclasses import dataclass
from datetime import datetime
from typing import Iterator

import numpy as np

from jldc.main import iter_jsonl, load_jsonl, save_jsonl
from tests.conftest import TEST_DIRECTORY


@dataclass
class _TestRecord:
    """Simple dataclass for testing purposes."""

    text: str
    number: int
    created: datetime
    array: np.ndarray


TEST_LIST = [
    _TestRecord(
        text="Alice",
        number=1,
        created=datetime(2023, 12, 10, 3, 3, 3),
        array=np.array([1, 2, 3]),
    ),
    _TestRecord(
        text="Bob",
        number=2,
        created=datetime(2024, 8, 7, 2, 2, 2),
        array=np.array([4.0, 5.0, 6.0]),
    ),
]


TEST_FILE = "test_file.jsonl"


TEST_PATH = f"{TEST_DIRECTORY}/{TEST_FILE}"


def test_save_then_load(create_directory):
    """Test the encoding/decoding cycle on a full file load."""
    save_jsonl(TEST_PATH, TEST_LIST)

    loaded_list = load_jsonl(TEST_PATH, _TestRecord)
    assert isinstance(loaded_list, list)

    for init, loaded in zip(TEST_LIST, loaded_list):
        assert init.text == loaded.text
        assert init.number == loaded.number
        assert init.created == loaded.created
        np.testing.assert_array_equal(init.array, loaded.array)


def test_save_then_iter(create_directory):
    """Test the encoding/decoding cycle when loading file as iterator."""
    save_jsonl(TEST_PATH, TEST_LIST)

    loaded_iter = iter_jsonl(TEST_PATH, _TestRecord)
    assert isinstance(loaded_iter, Iterator)

    idx = 0
    for loaded in loaded_iter:
        init = TEST_LIST[idx]
        assert init.text == loaded.text
        assert init.number == loaded.number
        assert init.created == loaded.created
        np.testing.assert_array_equal(init.array, loaded.array)
        idx += 1

    assert idx == 2
