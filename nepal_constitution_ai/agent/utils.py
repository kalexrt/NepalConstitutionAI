from langchain.agents import create_react_agent, AgentExecutor
from langchain_core.prompts import PromptTemplate

from nepal_constitution_ai.prompts.prompts import AGENT_PROMPT


def create_agent(
    llm_model, tools
):
    prompt = PromptTemplate.from_template(AGENT_PROMPT)
    agent = create_react_agent(
        llm_model, tools, prompt
    )

    return AgentExecutor(agent=agent, tools=tools, verbose=True)

