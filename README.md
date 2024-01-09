# Ionic Langchain

Ionic Langchain provides a wrapper around the Ionic Commerce's SDK for use as a `Tool` in a custom Langchain agent.  This tool will enable e-commerce for your agent, allowing your users to ask for product recommendations and purchase products through the agent chat interface.

## Installation

This tool requires at least `langchain@0.0.350` and can work with any greater patch release the `0.0.x` series.

We currently support python 3.8.10 and above, but if you need support for a lower version, please open an issue and we will add support.

You can install the package from PyPI using `pip`:

```sh
python3 -m pip install ionic-langchain
```

or `poetry`:

```sh
poetry add ionic-langchain
```

## Usage

```python
import os
from typing import List

from ionic_langchain.tool import IonicTool
from langchain.agents import AgentType, Tool
from langchain.agents import initialize_agent
from langchain.chat_models import ChatOpenAI

tools =  [
    IonicTool().tool(),
    # your other tools,
]

agent = initialize_agent(
    tools=tools,
    llm=ChatOpenAI(openai_api_key="your_key_here", temperature=0.7),
    agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    handle_parsing_errors=True,
    verbose=True,
)


input = "Where can I get tide pods"

agent.run(input=input)
```

_Please see the [langchain agent docs](https://python.langchain.com/docs/modules/agents/) for more details on how to build and run agents_

### Customizing the SDK

`ionic_langchain.tool.IonicTool`'s constructor accepts an instance of `ionic_langchain.tool.Ionic`, a wrapper around [our SDK](https://pypi.org/project/Ionic-API-SDK/).  `ionic_langchain.tool.Ionic`, in turn accepts an  instance of that SDK, so you can provide the tool with a custom configuration:

```python
import os
from ionic.sdk import Ionic as IonicSDK
from ionic_langchain.tool import Ionic, IonicTool


sdk = IonicSDK(api_key_header=os.environ.get("IONIC_API_KEY"))
ionic = Ionic(sdk=sdk)
tool = IonicTool(ionic=ionic).tool()
```

## Development

Coming soon. Please feel free to open an issue.
