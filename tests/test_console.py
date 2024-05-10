# tests/test_console.py
import click.testing
import pytest
from second import console

@pytest.fixture
def runner():
    return click.testing.CliRunner()

# def test_main_succeeds(runner):
#     result = runner.invoke(console.main)
#     assert result.exit_code == 0

@pytest.fixture
def mock_requests_get(mocker):
    mock = mocker.patch("requests.get")
    mock.return_value.__enter__.return_value.json.return_value = {
            "title": "Lorem Ipsum",
            "extract": "Lorem ipsum dolor sit amet",
    }
    return mock

def test_main_succeeds(runner, mock_requests_get):
    result = runner.invoke(console.main)
    assert result.exit_code == 0

def test_main_prints_title(runner, mock_requests_get):
    result = runner.invoke(console.main)
    assert "Lorem Ipsum" in result.output

def test_main_invokes_requests_get(runner, mock_requests_get):
    runner.invoke(console.main)
    assert mock_requests_get.called

def test_main_uses_correct_url(runner, mock_requests_get):
    runner.invoke(console.main)
    assert mock_requests_get.call_args == ((console.API_URL,),)

def test_main_fails_on_request_error(runner, mock_requests_get):
    mock_requests_get.side_effect = Exception("Boom")
    result = runner.invoke(console.main)
    assert result.exit_code == 1
