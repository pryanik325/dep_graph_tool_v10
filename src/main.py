

import sys
from config_parser import load_config, print_config, ConfigError
from npm_client import (
    fetch_package_info,
    extract_dependencies,
    NpmClientError
)


def _print_dependencies(deps: dict) -> None:

    if not deps:
        print("No direct dependencies found.")
        return

    print("--- Direct Dependencies ---")
    for name, version in deps.items():
        print(f"{name}: {version}")
    print("---------------------------")


def main() -> None:

    config_path = 'config.ini'

    if len(sys.argv) > 1:
        config_path = sys.argv[1]

    try:
        config = load_config(config_path)
        print_config(config)

        print("\nFetching package info...")
        pkg_info = fetch_package_info(
            config['repo_url'],
            config['package_name'],
            config['package_version'],
            config['test_mode']
        )

        deps = extract_dependencies(pkg_info)
        _print_dependencies(deps)

        print("\nStage 2 completed successfully.")
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