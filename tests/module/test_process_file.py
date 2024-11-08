import pytest
import os
from src.module.process_file import process_file

class TestProcessFile(object):
    def test_for_example_file(self, raw_and_clean_data_file):
        source_path, dest_path = raw_and_clean_data_file
        process_file(source_path, dest_path)
        with open(dest_path) as f:
            lines = f.readlines()
            first_line = lines[1]
            assert first_line == "2081,314942\n"
            second_line = lines[2]
            assert second_line == "1059,186606\n"

@pytest.fixture
def raw_and_clean_data_file(tmpdir):
    raw_data_file_path = tmpdir.join("raw.txt")
    clean_data_file_path = tmpdir.join("clean.txt")
    with open(raw_data_file_path, "w") as f:
        f.write("""area (sq. ft.)  price (dollars)
2,081	314,942
1,059	186,606
	 293,410
1,148	206,186
1,506	248,419
1,210	214,114
1,697	277,794
1,268	194,345
2,318	372,162
1,463238,765
1,468	239,007""")
    yield raw_data_file_path, clean_data_file_path  # No teardown code necessary
