import sys
from config_parser import load_config, print_config, ConfigError
from npm_client import NpmClientError
from graph_builder import build_dependency_graph


def _print_graph(graph: dict) -> None:
    print("\n--- Dependency Graph ---")
    for pkg, deps in graph.items():
        if deps:
            print(f"{pkg} -> {', '.join(deps)}")
        else:
            print(f"{pkg} -> (no dependencies)")
    print("------------------------")


def main() -> None:
    config_path = 'config.ini'

    if len(sys.argv) > 1:
        config_path = sys.argv[1]

    try:
        config = load_config(config_path)
        print_config(config)

        print("\nBuilding dependency graph...")
        graph = build_dependency_graph(
            config['package_name'],
            config
        )

        _print_graph(graph)

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