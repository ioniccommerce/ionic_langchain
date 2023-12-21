# Ionic Langchain

Ionic Langchain provides a wrapper around the Ionic Commerce's SDK for use as a `Tool` in a custom Langchain agent.  This tool will enable e-commerce for your agent, allowing your users to ask for product recommendations and purchase products through the agent chat interface.

## Installation

This tool requires at least `langchain@0.0.350` and can work with any greater patch release the `0.0.x` series.

You can install the package from GitHub using `pip`:

```sh
python3 -m pip install git+https://github.com/ioniccommerce/ionic_langchain.git#v0.1.2
```

or `poetry`:

```sh
poetry add git+https://github.com/ioniccommerce/ionic_langchain.git#v0.1.2
```

## Usage

```python
import os
from typing import List

from ionic_langchain.tool import IonicTool
from langchain.agents import AgentType, Tool
from langchain.agents import initialize_agent
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferWindowMemory, RedisChatMessageHistory


tools: List[Tool] =  [
    IonicTool().tool(),
    # others,
]
redis_memory = RedisChatMessageHistory(url=os.environ.get("REDIS_URL"),session_id="chatId"),
memory = ConversationBufferWindowMemory(
    k=12,
    return_messages=True,
    chat_memory=redis_memory,
    memory_key="chat_history",
)

agent = initialize_agent(
    tools=tools,
    llm=ChatOpenAI(openai_api_key=os.environ.get("OPENAI_API_KEY"),temperature=0.5),
    agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
    memory=memory,
    handle_parsing_errors=True,
    verbose=True,
)

agent.run(input="Roadhouse VHS")
```
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

Ionic Langchain is not currently accepting external contributions.  Contact us via [this form](https://ionicapi.com/contact) if you would like to contribute.
