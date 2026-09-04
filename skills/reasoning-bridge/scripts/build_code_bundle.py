#!/usr/bin/env python3
"""Build a minimal, sanitized ZIP for a Reasoning Bridge advisor request."""

from __future__ import annotations

import argparse
import re
import sys
import zipfile
from pathlib import Path


BLOCKED_PARTS = {
    ".git",
    ".hg",
    ".svn",
    ".cache",
    ".venv",
    "venv",
    "node_modules",
    "__pycache__",
    "build",
    "dist",
    "logs",
    "outputs",
    "checkpoints",
    "wandb",
}

BLOCKED_NAMES = {
    ".env",
    "credentials",
    "credentials.json",
    "cookies.json",
    "id_dsa",
    "id_ecdsa",
    "id_ed25519",
    "id_rsa",
    "secrets.json",
    "token.json",
}

BLOCKED_SUFFIXES = {
    ".ckpt",
    ".key",
    ".onnx",
    ".p12",
    ".pem",
    ".pfx",
    ".pickle",
    ".pkl",
    ".pt",
    ".pth",
    ".safetensors",
}

SECRET_PATTERNS = (
    re.compile(rb"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(rb"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(rb"\bgh[opurs]_[A-Za-z0-9]{20,}\b"),
    re.compile(rb"\bsk-[A-Za-z0-9_-]{20,}\b"),
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create an allowlist-based source bundle for a web advisor."
    )
    parser.add_argument("--root", required=True, type=Path, help="Repository root")
    parser.add_argument(
        "--include",
        action="append",
        required=True,
        help="File or directory relative to the repository root; repeat as needed",
    )
    parser.add_argument("--output", required=True, type=Path, help="New .zip path")
    parser.add_argument(
        "--max-file-bytes", type=int, default=1_000_000, help="Per-file size limit"
    )
    return parser.parse_args()


def relative_to_root(path: Path, root: Path) -> Path:
    resolved = path.resolve()
    try:
        return resolved.relative_to(root)
    except ValueError as exc:
        raise ValueError(f"Path leaves repository root: {path}") from exc


def blocked(relative: Path) -> str | None:
    lowered_parts = {part.lower() for part in relative.parts}
    if lowered_parts & BLOCKED_PARTS:
        return "blocked directory"
    name = relative.name.lower()
    if name in BLOCKED_NAMES or name.startswith(".env."):
        return "sensitive filename"
    if relative.suffix.lower() in BLOCKED_SUFFIXES:
        return "blocked binary or key format"
    return None


def collect(root: Path, includes: list[str]) -> list[Path]:
    selected: dict[str, Path] = {}
    for item in includes:
        candidate = (root / item).resolve()
        relative = relative_to_root(candidate, root)
        if not candidate.exists():
            raise ValueError(f"Included path does not exist: {relative}")
        paths = [candidate] if candidate.is_file() else candidate.rglob("*")
        for path in paths:
            if not path.is_file() or path.is_symlink():
                continue
            rel = relative_to_root(path, root)
            if blocked(rel):
                continue
            selected[rel.as_posix()] = path
    return [selected[key] for key in sorted(selected)]


def read_checked(path: Path, root: Path, max_bytes: int) -> tuple[Path, bytes]:
    relative = relative_to_root(path, root)
    size = path.stat().st_size
    if size > max_bytes:
        raise ValueError(f"File exceeds size limit ({size} bytes): {relative}")
    data = path.read_bytes()
    if b"\x00" in data:
        raise ValueError(f"Binary file is not allowed: {relative}")
    if any(pattern.search(data) for pattern in SECRET_PATTERNS):
        raise ValueError(f"Possible credential or private key found: {relative}")
    return relative, data


def main() -> int:
    args = parse_args()
    root = args.root.resolve()
    output = args.output.resolve()
    if not root.is_dir():
        print(f"Repository root is not a directory: {root}", file=sys.stderr)
        return 2
    if output.exists():
        print(f"Refusing to overwrite existing output: {output}", file=sys.stderr)
        return 2

    try:
        files = collect(root, args.include)
        checked = [read_checked(path, root, args.max_file_bytes) for path in files]
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    if not checked:
        print("No eligible files were selected.", file=sys.stderr)
        return 2

    output.parent.mkdir(parents=True, exist_ok=True)
    listing = "\n".join(f"- `{relative.as_posix()}`" for relative, _ in checked)
    note = (
        "# Code context\n\n"
        "This archive contains only the files selected for the current engineering "
        "decision. Read the accompanying advisor request for the goal, evidence, "
        "constraints, and questions.\n\n"
        "## Included files\n\n"
        f"{listing}\n"
    )

    with zipfile.ZipFile(output, "x", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("BRIDGE_CONTEXT.md", note)
        for relative, data in checked:
            archive.writestr(relative.as_posix(), data)

    print(output)
    print(f"Bundled {len(checked)} files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
