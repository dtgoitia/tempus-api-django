def pytest_configure(config):
    config.addinivalue_line(
        "markers", "focus: mark to target specific tests and skip the rest"
    )
