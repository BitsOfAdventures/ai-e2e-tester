"""
AI E2E Website Tester

Usage:
  ai_e2e_tester --url=<url> [--config=<str>] [--max-steps=<int>]

Options:
  --url=<url>           Landing page of the website to test.
  --config=<str>        Path to alternative configuration file.
  --max-steps=<int>     Maximum number of steps the AI can take while exploring the website [default: 5].
"""

from docopt import docopt

from ai_e2e_tester.agent import TestingAgent
from ai_e2e_tester.utils import setup_logging


def main():
    setup_logging()

    args = docopt(__doc__)
    url = args["--url"]
    config_path = args.get("--config") or "config.yml"
    max_steps = int(args['--max-steps'])

    agent = TestingAgent(url, config_path)
    agent.run(max_steps=max_steps)
