import pytest
from reconlib.core.exceptions import ReconLibException


class TestExceptions:
    @pytest.mark.parametrize("exception", ReconLibException.__subclasses__())
    def test_enumerator_exception(self, exception):
        """
        GIVEN the EnumeratorException base class
        WHEN one of its subclasses is raised
        THEN a given exception message and code must be present when the
            exception is raised
        """
        message = "Something went wrong"
        with pytest.raises(exception) as e:
            raise exception(message, code=1337)
        assert e.value.args[0] == f"{exception.__name__}: {message}"
        assert e.value.code == 1337
