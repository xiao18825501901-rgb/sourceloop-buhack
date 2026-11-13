"""Command-line entry point."""

from __future__ import annotations

import argparse
import logging
import webbrowser
from pathlib import Path

from sourceloop.app import create_server


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run the local SourceLoop study workspace."
    )
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=None,
        help="Runtime directory for the local SQLite database and logs.",
    )
    parser.add_argument(
        "--open",
        action="store_true",
        help="Open the local workspace in the default browser.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
    )
    server = create_server(
        host=args.host,
        port=args.port,
        runtime_dir=args.data_dir,
    )
    url = f"http://{args.host}:{server.server_address[1]}/"
    logging.info("SourceLoop is running at %s", url)
    logging.info("Runtime data: %s", server.application.runtime_dir.resolve())
    if args.open:
        webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        logging.info("Stopping SourceLoop")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
