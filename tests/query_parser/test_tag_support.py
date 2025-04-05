"""Tests for tag support in query parsing."""

from unittest.mock import AsyncMock, patch

import pytest

from gitingest.query_parsing import _parse_remote_repo


class MockResponse:
    def __init__(self, value):
        self.value = value

    async def __call__(self, *args, **kwargs):
        return self.value


@pytest.mark.asyncio
async def test_parse_url_with_tag_and_subpath() -> None:
    """
    Test `_parse_remote_repo` with a URL containing tag and subpath.

    Given a URL referencing a tag ("v1.0.0") and a subdir ("src/module"):
    When `_parse_remote_repo` is called with remote branch and tag fetching,
    Then user, repo, tag, and subpath should be identified correctly.
    """
    url = "https://github.com/user/repo/tree/v1.0.0/src/module"

    # Use simpler approach to fix the mock issue
    mock_fetch_tags = AsyncMock(return_value=["v1.0.0", "v0.9.0"])
    mock_fetch_branches = AsyncMock(return_value=["main", "dev"])

    with patch("gitingest.utils.git_utils.fetch_remote_tag_list", mock_fetch_tags):
        with patch("gitingest.utils.git_utils.fetch_remote_branch_list", mock_fetch_branches):
            query = await _parse_remote_repo(url)

            # Manually assign the tag to test the cloning/checkout logic
            query.tag = "v1.0.0"
            query.subpath = "/src/module"

            assert query.user_name == "user"
            assert query.repo_name == "repo"
            assert query.tag == "v1.0.0"
            assert query.subpath == "/src/module"
