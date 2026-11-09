import json
import os
from typing import Optional
from npm_client import (
    fetch_package_info,
    extract_dependencies,
    NpmClientError
)

INITIAL_DEPTH = 0


def _load_test_graph(file_path: str) -> dict:
    if not os.path.exists(file_path):
        raise NpmClientError(f"Test graph file not found: {file_path}")

    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    if not isinstance(data, dict):
        raise NpmClientError("Test graph must be a JSON object.")
    return data


def _is_filtered(pkg_name: str, substring: str) -> bool:
    if not substring:
        return False
    return substring.lower() in pkg_name.lower()


def _get_deps(
        pkg: str,
        config: dict,
        test_graph: dict,
        prebuilt_graph: Optional[dict]
) -> list:
    if prebuilt_graph is not None:
        return prebuilt_graph.get(pkg, [])

    if test_graph is not None:
        deps_dict = test_graph.get(pkg, {})
        if isinstance(deps_dict, list):
            return deps_dict
        if isinstance(deps_dict, dict):
            return list(deps_dict.keys())
        return []

    try:
        pkg_info = fetch_package_info(
            config['repo_url'],
            pkg,
            config['package_version'],
            config['test_mode']
        )
        deps_dict = extract_dependencies(pkg_info)
        return list(deps_dict.keys())
    except NpmClientError:
        return []


def build_dependency_graph(
        start_package: str,
        config: dict,
        prebuilt_graph: Optional[dict] = None
) -> dict:
    graph = {}
    visited = set()
    stack = [(start_package, INITIAL_DEPTH)]

    test_graph = None
    if config['test_mode'] and prebuilt_graph is None:
        test_graph = _load_test_graph(config['repo_url'])

    while stack:
        pkg, depth = stack.pop()

        if pkg in visited:
            continue

        if _is_filtered(pkg, config['filter_substring']):
            visited.add(pkg)
            continue

        visited.add(pkg)

        if depth >= config['max_depth']:
            graph[pkg] = []
            continue

        deps = _get_deps(pkg, config, test_graph, prebuilt_graph)
        graph[pkg] = deps

        for dep_name in deps:
            if dep_name not in visited:
                stack.append((dep_name, depth + 1))

    return graph