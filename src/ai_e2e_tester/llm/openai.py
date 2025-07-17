import json
import logging
from typing import List, Dict

import openai

from ai_e2e_tester.browser.next_step import NextStep
from ai_e2e_tester.llm.ai_wrapper import AiWrapper

logger = logging.getLogger('ai-e2e-tester.llm')


class OpenAiWrapper(AiWrapper):
    """
    A wrapper to call the LLM.
    Currently only OpenAI is supported.
    """

    def __init__(self, api_key, user_prompt_template, max_tokens=400):
        self.max_tokens = max_tokens
        self.user_prompt_template = user_prompt_template
        self.client = openai.OpenAI(api_key=api_key)

    def run(self, page_html: str, screenshot_b64, prev_steps: List[NextStep]) -> Dict:
        """
        @todo Will be better to interact with screenshot instead of text to also access style.
        @todo Add system prompt to config file
        :param prev_steps:
        :param page_html:
        :param screenshot_b64:
        :return:
        """

        user_prompt = self.user_prompt_template.format(
            page_html=page_html,
            prev_actions=" then ".join([str(step) for step in prev_steps])
        )

        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a smart website tester."},
                {"role": "user", "content": user_prompt},
            ],
            max_tokens=self.max_tokens,
            temperature=0.2,
        )

        txt = response.choices[0].message.content.strip()

        try:
            result = json.loads(txt)
        except Exception:
            logger.warning(f"Failed to parse response as JSON: {txt}")
            result = {
                "next_step": {"action": "done"},
                "reason": "Parsing error of JSON output from AI.",
                "bugs": [],
                "suggestions": []
            }
        return result
