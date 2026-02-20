#!/usr/bin/env python3
"""
Diagnostics script to collect system information and environment variables.
Writes the collected information to diagnostics.txt for debugging purposes.
"""

import os
import platform
import sys
import datetime


def collect_diagnostics():
    """Collect system and environment diagnostics."""
    lines = []

    lines.append("=" * 60)
    lines.append("SYSTEM DIAGNOSTICS")
    lines.append("=" * 60)
    lines.append(f"Generated: {datetime.datetime.now(datetime.UTC).isoformat()}")
    lines.append("")

    lines.append("SYSTEM INFORMATION:")
    lines.append("-" * 60)
    lines.append(f"Platform: {platform.platform()}")
    lines.append(f"System: {platform.system()}")
    lines.append(f"Release: {platform.release()}")
    lines.append(f"Version: {platform.version()}")
    lines.append(f"Machine: {platform.machine()}")
    lines.append(f"Processor: {platform.processor()}")
    lines.append(f"Python Version: {sys.version}")
    lines.append(f"Python Executable: {sys.executable}")
    lines.append("")

    lines.append("ENVIRONMENT VARIABLES:")
    lines.append("-" * 60)

    relevant_prefixes = [
        'E2E_',
        'GITHUB_',
        'CI',
        'PYTHON',
        'PATH',
        'HOME',
        'USER',
        'LANG',
        'TZ',
        'WORKSPACE',
    ]

    env_vars = {}
    for key, value in os.environ.items():
        if any(key.startswith(prefix) for prefix in relevant_prefixes):
            env_vars[key] = value

    if env_vars:
        for key in sorted(env_vars.keys()):
            value = env_vars[key]
            if 'TOKEN' in key or 'SECRET' in key or 'PASSWORD' in key or 'KEY' in key:
                if value:
                    masked_value = value[:4] + '*' * (len(value) - 4) if len(value) > 4 else '*' * len(value)
                else:
                    masked_value = '(empty)'
                lines.append(f"{key}={masked_value}")
            else:
                lines.append(f"{key}={value}")
    else:
        lines.append("No relevant environment variables found.")

    lines.append("")
    lines.append("=" * 60)

    return "\n".join(lines)


def write_diagnostics(output_file='diagnostics.txt'):
    """Write diagnostics to file."""
    content = collect_diagnostics()
    with open(output_file, 'w') as f:
        f.write(content)
    return output_file


def main():
    """Main entry point."""
    output_file = write_diagnostics()
    print(f"Diagnostics written to {output_file}")
    print("\nPreview:")
    print("-" * 60)
    with open(output_file, 'r') as f:
        print(f.read())


if __name__ == '__main__':
    main()
