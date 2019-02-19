import pytest
from colour import Color

from src.color_list import ColorList


class Test_ColorList:
    def test_empty(self):
        color_list = ColorList()
        with pytest.raises(KeyError):
            color_list[0]

    def test_new(self):
        color_list = ColorList()
        color_list.new()
        assert(color_list[0] == Color('black'))

    def test_edit(self):
        color_list = ColorList()
        color_list.new()
        assert(color_list[0] == Color('black'))
        color_list[0].rgb = (1, 1, 1)
        assert(color_list[0] == Color('white'))

    def test_delete(self):
        color_list = ColorList()
        color_list.new()
        del color_list[0]
        with pytest.raises(KeyError):
            color_list[0]
        color_list.new()
        with pytest.raises(KeyError):
            color_list[0]
        assert(color_list[1] == Color('black'))
