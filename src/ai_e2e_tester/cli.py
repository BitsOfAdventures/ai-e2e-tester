"""
AI E2E Website Tester

Usage:
  ai_e2e_tester --url=<url> [--config=<str>]
"""
import os

from docopt import docopt

from ai_e2e_tester.agent import TestingAgent
from ai_e2e_tester.utils import setup_logging


def main():
    setup_logging()

    args = docopt(__doc__)
    url = args["--url"]
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("Error: No API key found. Please set the OPENAI_API_KEY environment variable.")
        return
    config_path = args.get("--config") or "config.yml"
    agent = TestingAgent(url, api_key, config_path)
    agent.run(max_steps=20)
