from langchain.base_language import BaseLanguageModel
from langchain_experimental.autonomous_agents.hugginggpt.repsonse_generator import (
    load_response_generator,
)
from langchain_experimental.autonomous_agents.hugginggpt.task_executor import (
    TaskExecutor,
)
from langchain_experimental.autonomous_agents.hugginggpt.task_planner import (
    load_chat_planner,
)
# from transformers import load_tool  # Deprecated in newer transformers versions
try:
    from transformers import load_tool
except ImportError:
    # Handle gracefully for newer transformers versions
    def load_tool(*args, **kwargs):
        """
        Fallback function for `load_tool` in newer versions of the `transformers` library.
        
        This function is defined to handle cases where the `load_tool` function is not
        available in the installed version of `transformers`. It raises an ImportError
        to indicate that the functionality is not supported.
        
        Args:
            *args: Positional arguments (not used).
            **kwargs: Keyword arguments (not used).
        
        Raises:
            ImportError: Always raised to indicate `load_tool` is unavailable.
        """
        raise ImportError("load_tool is not available in this transformers version")

from swarms.structs.agent import Agent
from swarms.utils.loguru_logger import logger


class OmniModalAgent(Agent):
    """
    OmniModalAgent
    LLM -> Plans -> Tasks -> Tools -> Response

    Architecture:
    1. LLM: Language Model
    2. Chat Planner: Plans
    3. Task Executor: Tasks
    4. Tools: Tools

    Args:
        llm (BaseLanguageModel): Language Model
        tools (List[BaseTool]): List of tools

    Returns:
        str: response

    Usage:
    from swarms import OmniModalAgent, OpenAIChat,

    llm = OpenAIChat()
    agent = OmniModalAgent(llm)
    response = agent.run("Hello, how are you? Create an image of how your are doing!")
    """

    def __init__(
        self,
        llm: BaseLanguageModel,
        verbose: bool = False,
        *args,
        **kwargs,
    ):
        super().__init__(llm=llm, *args, **kwargs)
        self.llm = llm
        self.verbose = verbose

        print("Loading tools...")
        self.tools = [
            load_tool(tool_name)
            for tool_name in [
                "document-question-answering",
                "image-captioning",
                "image-question-answering",
                "image-segmentation",
                "speech-to-text",
                "summarization",
                "text-classification",
                "text-question-answering",
                "translation",
                "huggingface-tools/text-to-image",
                "huggingface-tools/text-to-video",
                "text-to-speech",
                "huggingface-tools/text-download",
                "huggingface-tools/image-transformation",
            ]
        ]

        # Load the chat planner and response generator
        self.chat_planner = load_chat_planner(llm)
        self.response_generator = load_response_generator(llm)
        self.task_executor = TaskExecutor
        self.history = []

    def run(self, task: str) -> str:
        """Run the OmniAgent"""
        try:
            plan = self.chat_planner.plan(
                inputs={
                    "input": task,
                    "hf_tools": self.tools,
                }
            )
            self.task_executor = TaskExecutor(plan)
            self.task_executor.run()

            response = self.response_generator.generate(
                {"task_execution": self.task_executor}
            )

            return response
        except Exception as error:
            logger.error(f"Error running the agent: {error}")
            return f"Error running the agent: {error}"
