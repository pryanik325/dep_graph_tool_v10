

import sys
from config_parser import load_config, print_config, ConfigError


def main() -> None:

    config_path = 'config.ini'

    if len(sys.argv) > 1:
        config_path = sys.argv[1]

    try:
        config = load_config(config_path)
        print_config(config)
        print("Stage 1 completed successfully.")
    except ConfigError as e:
        print(f"Config Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()