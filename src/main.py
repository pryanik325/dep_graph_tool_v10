"""Main entry point for the dependency graph tool."""

import sys
from config_parser import load_config, print_config, ConfigError
from npm_client import NpmClientError
from graph_builder import (
    build_dependency_graph,
    invert_graph,
    _load_test_graph
)


def _print_graph(graph: dict) -> None:
    """Print the dependency graph to the console."""
    for pkg, deps in graph.items():
        if deps:
            print(f"{pkg} -> {', '.join(deps)}")
        else:
            print(f"{pkg} -> (no dependencies)")


def main() -> None:
    """Execute the main logic of the application."""
    config_path = 'config.ini'

    if len(sys.argv) > 1:
        config_path = sys.argv[1]

    try:
        config = load_config(config_path)
        print_config(config)

        print("\n--- Forward Dependency Graph ---")
        graph = build_dependency_graph(config['package_name'], config)
        _print_graph(graph)

        # Демонстрация Этапа 4: Обратные зависимости
        print("\n--- Reverse Dependency Graph ---")
        if config['test_mode']:
            full_test_graph = _load_test_graph(config['repo_url'])
            normalized = {}
            for pkg, deps in full_test_graph.items():
                if isinstance(deps, list):
                    normalized[pkg] = deps
                elif isinstance(deps, dict):
                    normalized[pkg] = list(deps.keys())
                else:
                    normalized[pkg] = []
            inverted = invert_graph(normalized)
        else:
            inverted = invert_graph(graph)

        reverse_graph = build_dependency_graph(
            config['package_name'],
            config,
            prebuilt_graph=inverted
        )
        _print_graph(reverse_graph)

        print("\nStage 4 completed successfully.")

    except ConfigError as e:
        print(f"Config Error: {e}", file=sys.stderr)
        sys.exit(1)
    except NpmClientError as e:
        print(f"Client Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()