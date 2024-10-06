from langchain.agents import create_react_agent, AgentExecutor
from langchain_core.prompts import PromptTemplate
from nepal_constitution_ai.models.openai.openai_model import OpenaiModel
from nepal_constitution_ai.models.groq.groq_model import GroqModel
from typing import Union
from nepal_constitution_ai.prompts.prompts import AGENT_PROMPT
from langchain.tools import Tool


def create_agent(
    llm_model: Union[OpenaiModel, GroqModel], tools: list[Tool]
):
    prompt = PromptTemplate.from_template(AGENT_PROMPT)
    agent = create_react_agent(
        llm_model, tools, prompt
    )

    return AgentExecutor(agent=agent, tools=tools, verbose=True)

