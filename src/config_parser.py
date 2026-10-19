

import configparser
import os

MIN_DEPTH = 1


class ConfigError(Exception):

    pass


def _parse_bool(value: str, key: str) -> bool:

    lower_val = value.lower()
    if lower_val in ('true', '1', 'yes'):
        return True
    if lower_val in ('false', '0', 'no'):
        return False
    raise ConfigError(f"Invalid boolean for {key}: {value}")


def _parse_int(value: str, key: str, min_val: int) -> int:

    try:
        val = int(value)
    except ValueError:
        raise ConfigError(f"Invalid integer for {key}: {value}")

    if val < min_val:
        raise ConfigError(f"{key} must be >= {min_val}")
    return val


def _check_required_keys(section: configparser.SectionProxy) -> None:

    required_keys = [
        'package_name', 'repo_url', 'test_mode',
        'package_version', 'ascii_tree', 'max_depth',
        'filter_substring'
    ]
    for key in required_keys:
        if key not in section:
            raise ConfigError(f"Missing required key: {key}")


def load_config(file_path: str) -> dict:

    if not os.path.exists(file_path):
        raise ConfigError(f"Config file not found: {file_path}")

    parser = configparser.ConfigParser()
    parser.read(file_path, encoding='utf-8')

    if 'Settings' not in parser:
        raise ConfigError("Missing [Settings] section.")

    section = parser['Settings']
    _check_required_keys(section)

    config = {
        'package_name': section['package_name'].strip(),
        'repo_url': section['repo_url'].strip(),
        'test_mode': _parse_bool(section['test_mode'], 'test_mode'),
        'package_version': section['package_version'].strip(),
        'ascii_tree': _parse_bool(section['ascii_tree'], 'ascii_tree'),
        'max_depth': _parse_int(
            section['max_depth'], 'max_depth', MIN_DEPTH
        ),
        'filter_substring': section['filter_substring'].strip()
    }

    if not config['package_name']:
        raise ConfigError("package_name cannot be empty.")

    return config


def print_config(config: dict) -> None:

    print("--- Current Configuration ---")
    for key, value in config.items():
        print(f"{key}: {value}")
    print("-----------------------------")