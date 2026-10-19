
import json
import urllib.request
import urllib.error
import os

REQUEST_TIMEOUT = 10


class NpmClientError(Exception):

    pass


def _read_from_file(file_path: str) -> dict:

    if not os.path.exists(file_path):
        raise NpmClientError(f"Test file not found: {file_path}")

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        raise NpmClientError(f"Invalid JSON in file: {e}")


def _fetch_from_url(url: str) -> dict:

    try:
        req = urllib.request.Request(url)
        req.add_header('Accept', 'application/json')

        with urllib.request.urlopen(
                req, timeout=REQUEST_TIMEOUT
        ) as response:
            data = response.read().decode('utf-8')
            return json.loads(data)

    except urllib.error.HTTPError as e:
        raise NpmClientError(f"HTTP error {e.code}: {e.reason}")
    except urllib.error.URLError as e:
        raise NpmClientError(f"URL error: {e.reason}")
    except json.JSONDecodeError as e:
        raise NpmClientError(f"Invalid JSON response: {e}")


def fetch_package_info(
        repo_url: str,
        package_name: str,
        version: str,
        test_mode: bool
) -> dict:

    if test_mode:
        return _read_from_file(repo_url)

    base_url = repo_url if repo_url.endswith('/') else repo_url + '/'
    url = f"{base_url}{package_name}/{version}"

    return _fetch_from_url(url)


def extract_dependencies(package_info: dict) -> dict:

    if not isinstance(package_info, dict):
        raise NpmClientError("Invalid package info format.")

    deps = package_info.get('dependencies', {})
    if not isinstance(deps, dict):
        raise NpmClientError("Dependencies section is not a dict.")

    return deps