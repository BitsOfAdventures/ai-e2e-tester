# 🤖 AI E2E Website Tester

Skip the test scripts. Just point the AI E2E Website Tester at your website, and watch it explore it.

The AI acts like a real human visitor, clicking, scrolling, and reading your website. As it goes, it automatically takes notes on bugs, UX issues, and proposes suggestions.

This tool is an early prototype.

Feedback and ideas are very welcome!

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