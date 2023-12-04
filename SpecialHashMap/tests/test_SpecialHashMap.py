import pytest
from ..src.SpecialHashMap import SpecialHashMap


@pytest.fixture(scope="function")
def shmap():
    return SpecialHashMap()


class TestSpecialHashMap:
    shmap = SpecialHashMap()

    def test_value(self, shmap):
        shmap["value1"] = 1
        shmap["value2"] = 2
        shmap["value3"] = 3

        assert shmap["value1"] == 1
        assert shmap["value2"] == 2
        assert shmap["value3"] == 3

    def test_iloc(self, shmap):

        shmap["value1"] = 1
        shmap["value2"] = 2
        shmap["value3"] = 3
        shmap["1"] = 10
        shmap["2"] = 20
        shmap["3"] = 30
        shmap["1, 5"] = 100
        shmap["5, 5"] = 200
        shmap["10, 5"] = 300

        assert shmap.iloc[0] == 10
        assert shmap.iloc[2] == 300
        assert shmap.iloc[5] == 200
        assert shmap.iloc[8] == 3

    def test_wrong_key(self, shmap):
        shmap["1"] = 10
        shmap["2"] = 20
        shmap["3"] = 30
        with pytest.raises(IndexError):
            assert shmap.iloc[5]

    def test_ploc(self, shmap):
        shmap["value1"] = 1
        shmap["value2"] = 2
        shmap["value3"] = 3
        shmap["1"] = 10
        shmap["2"] = 20
        shmap["3"] = 30
        shmap["(1, 5)"] = 100
        shmap["(5, 5)"] = 200
        shmap["(10, 5)"] = 300
        shmap["(1, 5, 3)"] = 400
        shmap["(5, 5, 4)"] = 500
        shmap["(10, 5, 5)"] = 600

        assert shmap.ploc[">=1"] == {"1": 10, "2": 20, "3": 30}
        assert shmap.ploc[">1"] == {"2": 20, "3": 30}
        assert shmap.ploc["<=1"] == {"1": 10}
        assert shmap.ploc["=1"] == {"1": 10}
        assert shmap.ploc["<>1"] == {"2": 20, "3": 30}
        assert shmap.ploc["<3"] == {"1": 10, "2": 20}
        assert shmap.ploc[">0, >0"] == {"(1, 5)": 100, "(5, 5)": 200, "(10, 5)": 300}
        assert shmap.ploc[">=10, >0"] == {"(10, 5)": 300}
        assert shmap.ploc["<5, >=5, >=3"] == {"(1, 5, 3)": 400}

    def test_invalid_operator(self, shmap):
        shmap["1"] = 10
        shmap["2"] = 20
        shmap["3"] = 30
        with pytest.raises(ValueError):
            assert shmap.ploc["*1"]
