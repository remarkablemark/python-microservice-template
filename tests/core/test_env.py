"""Tests for environment variable utilities."""

from app.core.env import get_env_bool, get_env_list, get_env_str
from tests.utils.env import temporary_env_vars


def test_get_env_bool_true() -> None:
    """Test get_env_bool returns True for 'true' value."""
    with temporary_env_vars(TEST_BOOL="true"):
        assert get_env_bool("TEST_BOOL") is True


def test_get_env_bool_true_case_insensitive() -> None:
    """Test get_env_bool is case insensitive."""
    with temporary_env_vars(TEST_BOOL="True"):
        assert get_env_bool("TEST_BOOL") is True

    with temporary_env_vars(TEST_BOOL="TRUE"):
        assert get_env_bool("TEST_BOOL") is True


def test_get_env_bool_false() -> None:
    """Test get_env_bool returns False for non-'true' values."""
    with temporary_env_vars(TEST_BOOL="false"):
        assert get_env_bool("TEST_BOOL") is False

    with temporary_env_vars(TEST_BOOL="1"):
        assert get_env_bool("TEST_BOOL") is False

    with temporary_env_vars(TEST_BOOL="yes"):
        assert get_env_bool("TEST_BOOL") is False


def test_get_env_bool_default_false() -> None:
    """Test get_env_bool returns default False when not set."""
    with temporary_env_vars(TEST_BOOL=None):
        assert get_env_bool("TEST_BOOL") is False


def test_get_env_bool_default_true() -> None:
    """Test get_env_bool returns custom default when not set."""
    with temporary_env_vars(TEST_BOOL=None):
        assert get_env_bool("TEST_BOOL", default=True) is True


def test_get_env_str_default() -> None:
    """Test get_env_str returns default when not set."""
    with temporary_env_vars(TEST_STR=None):
        assert get_env_str("TEST_STR") == ""
        assert get_env_str("TEST_STR", "default") == "default"


def test_get_env_str_value() -> None:
    """Test get_env_str returns value when set."""
    with temporary_env_vars(TEST_STR="test-value"):
        assert get_env_str("TEST_STR") == "test-value"


def test_get_env_list_default() -> None:
    """Test get_env_list returns default when not set."""
    with temporary_env_vars(TEST_LIST=None):
        assert get_env_list("TEST_LIST") == []
        assert get_env_list("TEST_LIST", default=["a", "b"]) == ["a", "b"]


def test_get_env_list_comma_separated() -> None:
    """Test get_env_list parses comma-separated values."""
    with temporary_env_vars(TEST_LIST="token1,token2,token3"):
        assert get_env_list("TEST_LIST") == ["token1", "token2", "token3"]


def test_get_env_list_with_whitespace() -> None:
    """Test get_env_list strips whitespace."""
    with temporary_env_vars(TEST_LIST=" token1 , token2 , token3 "):
        assert get_env_list("TEST_LIST") == ["token1", "token2", "token3"]


def test_get_env_list_empty_strings_filtered() -> None:
    """Test get_env_list filters out empty strings."""
    with temporary_env_vars(TEST_LIST="token1,,token2,  ,token3"):
        assert get_env_list("TEST_LIST") == ["token1", "token2", "token3"]


def test_get_env_list_custom_separator() -> None:
    """Test get_env_list with custom separator."""
    with temporary_env_vars(TEST_LIST="token1;token2;token3"):
        assert get_env_list("TEST_LIST", separator=";") == [
            "token1",
            "token2",
            "token3",
        ]
