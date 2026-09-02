import pytest

from utils import calculate_percent_change, should_alert


@pytest.mark.parametrize(
    "current_price,base_price,expected",
    [
        (110, 100, 10.0),        # рост на 10%
        (90, 100, -10.0),        # падение на 10%
        (100, 100, 0.0),         # цена не изменилась
        (101, 100, 1.0),         # рост на 1% (на границе порога)
        (102.5, 100, 2.5),       # дробный случай
        (0, 100, -100.0),        # цена упала до нуля
    ],
)
def test_calculate_percent_change(current_price, base_price, expected):
    result = calculate_percent_change(current_price, base_price)
    assert result == pytest.approx(expected)


def test_calculate_percent_change_zero_base_raises():
    """Базовая цена не может быть нулевой — деление на ноль невозможно."""
    with pytest.raises(ValueError):
        calculate_percent_change(100, 0)


def test_calculate_percent_change_negative_base_raises():
    with pytest.raises(ValueError):
        calculate_percent_change(100, -50)


@pytest.mark.parametrize(
    "percent_change,threshold,expected",
    [
        (5.0, 1.0, True),        # превышение порога
        (-5.0, 1.0, True),       # превышение вниз
        (5.0, 5.0, True),        # ровно на пороге — срабатывает
        (-5.0, 5.0, True),       # ровно на пороге (вниз)
        (0.9, 1.0, False),       # ниже порога
        (-0.9, 1.0, False),      # ниже порога (вниз)
        (0.0, 0.5, False),       # без изменений
    ],
)
def test_should_alert(percent_change, threshold, expected):
    assert should_alert(percent_change, threshold) is expected