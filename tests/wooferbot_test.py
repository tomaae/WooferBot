import pytest

def sum(num1, num2):
	return num1 + num2

def test_sum():
	assert sum(1, 2) == 3