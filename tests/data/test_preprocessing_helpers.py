from src.data.preprocessing_helpers import row_to_list, convert_to_int

class TestRowToList(object):
    def test_for_clean_row(self):
        assert row_to_list("2,081\t314,942\n") == ["2,081", "314,942"]
    def test_for_missing_area(self):
        assert row_to_list("\t293,410\n") is None
    def test_for_missing_tab(self):
        assert row_to_list("1,463238,765\n") is None

class TestConvertToInt(object):
    def test_with_no_comma(self):
        assert convert_to_int("2081") == 2081
    def test_with_one_comma(self):
        assert convert_to_int("2,081") == 2081
