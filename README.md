# 🤖 AI E2E Website Tester

Skip the test scripts. Just point the AI E2E Website Tester at your website, and watch it explore it.

The AI acts like a real human visitor, clicking, scrolling, and reading your website. As it goes, it automatically takes notes on bugs, UX issues, and proposes suggestions.

This tool is an early prototype.

Feedback and ideas are very welcome!

---

## Example run

```console
ai-e2e-tester.agent - INFO - Test started. Max steps: 6
ai-e2e-tester.agent - INFO - [Step 1] On Page: https://pi-match.web.app/
ai-e2e-tester.agent - INFO - Current goal: Find a suitable PI and lab based on location and interests.
ai-e2e-tester.browser.next_step - INFO - Reasoning for Next Action: To initiate a search for PIs and labs.
ai-e2e-tester.agent - INFO - Typed "Melbourne" into field "affiliation_input" → Page content updated.
ai-e2e-tester.agent - INFO - [Step 2] On Page: https://pi-match.web.app/
ai-e2e-tester.agent - INFO - Current goal: Find a suitable PI and lab based on location and interests.
ai-e2e-tester.browser.next_step - INFO - Reasoning for Next Action: To attempt a search with interests included.
ai-e2e-tester.agent - INFO - Typed "epigenetics" into field "What I like" → Page content updated.
ai-e2e-tester.agent - INFO - [Step 3] On Page: https://pi-match.web.app/
ai-e2e-tester.agent - INFO - Current goal: Find a suitable PI and lab based on location and interests.
ai-e2e-tester.browser.next_step - INFO - Reasoning for Next Action: To initiate the search based on entered criteria.
ai-e2e-tester.agent - INFO - Clicked on "Search" → Navigated to new URL.
ai-e2e-tester.agent - INFO - [Step 4] On Page: https://pi-match.web.app/labs?location=Melbourne&keywords=epigenetics
ai-e2e-tester.agent - INFO - Current goal: Find a suitable PI and lab in Melbourne related to epigenetics.
ai-e2e-tester.browser.next_step - INFO - Reasoning for Next Action: The page is still loading; waiting may allow results to appear.
ai-e2e-tester.browser.actions.wait - INFO - → Waiting 20sec for the page to be ready
ai-e2e-tester.agent - INFO - Waited for 20sec. → Page content updated.
ai-e2e-tester.agent - INFO - [Step 5] On Page: https://pi-match.web.app/labs?location=Melbourne&keywords=epigenetics
ai-e2e-tester.agent - INFO - Current goal: Find labs related to epigenetics in Melbourne.
ai-e2e-tester.browser.next_step - INFO - Reasoning for Next Action: Explore more details about a specific lab.

```


---

## 🛠️ Installation

Clone this repo and install dependencies:

```bash
git clone https://github.com/BitsOfAdventures/ai-e2e-tester.git
cd ai-e2e-tester

pip install -r requirements/base.txt
playwright install
````


## 🚀 Quick Start

Set your API key as an environment variable:

```bash
export OPENAI_API_KEY=sk-...       # On macOS/Linux
```

Then run the tool from the project root:

```bash
python -m src.ai_e2e_tester --url=https://example.com
```


## 💬 Feedback Wanted
This is an early prototype. If you try it, please open an issue or suggest improvements, any feedback is appreciated!

## Currently Supported Actions
Here is what the agent can currently do on the tested website:

- Click on links, buttons, etc..
- Type text into input fields
- Navigate to the previous page
- Scroll down
- Wait while the page is loading data from the server