import json
import logging
import os
from typing import Dict

import openai

from ai_e2e_tester.llm.ai_wrapper import AiWrapper

logger = logging.getLogger('ai-e2e-tester.llm')


class OpenAiWrapper(AiWrapper):
    """
    A wrapper to call the LLM.
    Currently only OpenAI is supported.
    """

    def __init__(self, prompts:Dict[str, str], max_tokens=800):
        self.max_tokens = max_tokens
        self.prompts = prompts

        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise Exception("No API key found. Please set the OPENAI_API_KEY environment variable.")

        self.client = openai.OpenAI(api_key=api_key)

    def run(self, page_url: str, page_html: str, screenshot_b64, context: str, available_actions: str) -> Dict:
        """

        :param page_url:
        :param context:
        :param page_html:
        :param screenshot_b64:
        :param available_actions
        :return:
        """

        system_prompt = self.prompts['system']

        user_prompt = self.prompts['user'].format(
            page_url=page_url,
            page_html=page_html,
            context=context,
            available_actions=available_actions
        )

        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": user_prompt},
                        {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{screenshot_b64}"}}
                    ]
                }
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
