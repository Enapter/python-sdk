import sys
from unittest.mock import MagicMock

# The enapter package's __init__.py imports all core submodules (async_, log, mdns, mqtt, http, standalone).
# This means that importing even a small part of the package (like Labels) can trigger
# imports of all dependencies. We mock these dependencies to allow unit tests to run in
# environments where they are not installed.
MOCKED_MODULES = [
    "json_log_formatter",
    "aiomqtt",
    "httpx",
    "dns",
    "dns.asyncresolver",
    "docker",
]

for module_name in MOCKED_MODULES:
    if module_name not in sys.modules:
        sys.modules[module_name] = MagicMock()
