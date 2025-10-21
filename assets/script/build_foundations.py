"""
Scan fossfoundation/_foundations and make _config.yml hash
Usage:
    python3 build_foundations.py ../fossfoundation/_foundations
"""

import argparse
import sys
from pathlib import Path
import yaml

YAML_SEPARATOR = '---'

def parse_frontmatter(file_path: Path) -> dict | None:
    """
    Parse file and return relevant frontmatter, otherwise None.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        parts = content.split(YAML_SEPARATOR)
        if len(parts) < 3 or parts[0].strip() != '':
            # Not a valid Jekyll post with frontmatter at the top.
            print(
                f"WARN: Skipping {file_path.name}: "
                "No frontmatter found.", file=sys.stderr
            )
            return None
        frontmatter = parts[1]
        data = yaml.safe_load(frontmatter)
        # Ensure the frontmatter parsed into a dictionary and has our keys.
        if isinstance(data, dict):
            return {
                'identifier': data['identifier'],
                'commonName': data['commonName']
            }
        else:
            print(
                f"WARN: Skip {file_path.name}: "
                "Missing fields in frontmatter.",
                file=sys.stderr
            )
            return None
    except Exception as e:
        print(
            f"ERROR: file read {file_path.name}: {e}",
            file=sys.stderr
        )
    return None

def parse_dir(file_path: Path):
    all_data = []
    for file_path in sorted(scanpath.glob('*.md')):
        data = parse_frontmatter(file_path)
        if data:
            all_data.append(data)

    if not all_data:
        print("No valid Jekyll posts with relevant fields found.")
        return

    return {'foundations': all_data}

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description= 'Scan directory for *.md files and parse selected Jekyll frontmatter.'
    )
    parser.add_argument(
        'directory',
        type=str,
        help='The path to the directory to scan.'
    )
    args = parser.parse_args()
    scanpath = Path(args.directory)
    if not scanpath.is_dir():
        print(f"ERROR: path '{scanpath}' is not valid dir.", file=sys.stderr)
        sys.exit(1)
    output = parse_dir(scanpath)
    print(yaml.dump(output, sort_keys=False, indent=4))
