"""
Global test configuration.
"""

from collections.abc import Sequence

import pytest


def pytest_collection_modifyitems(config: pytest.Config, items: Sequence[pytest.Item]):
    """
    Adds test type markers to all collected tests, based on their top-level package.

    :param config: The test config
    :param items: The collected items
    """

    root_path = config.rootpath / "tests"
    for item in items:
        # Sanity check
        if not item.path.is_relative_to(root_path):
            raise RuntimeError("Item is not contained in root path")

        rel_path = item.path.relative_to(root_path)
        test_type = rel_path.parts[0]
        item.add_marker(getattr(pytest.mark, test_type))
