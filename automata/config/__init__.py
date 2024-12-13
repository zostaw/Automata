"""Configuration file for the program.

This file defines environment variables that are used by the program to interact with various APIs, as well as constants that are used throughout the program.

Environment variables:
- GITHUB_API_KEY: The API key for the GitHub API.
- OPENAI_API_KEY: The API key for the OpenAI API.
- CONVERSATION_DB_PATH: The abs path to use for storing conversation data.
- TASK_DB_PATH: The output path for new tasks.
- MAX_WORKERS: The maximum number of workers to run concurrently.

Note that the environment variables are loaded from a .env file using the `load_dotenv()` function from the `dotenv` library.
"""

import os

from dotenv import load_dotenv

from automata.config.config_base import (
    AgentConfig,
    LLMProvider,
    ModelInformation,
)
from automata.config.openai_config import OpenAIAutomataAgentConfig

load_dotenv()

# Define environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
GITHUB_API_KEY = os.getenv("GITHUB_API_KEY", "")
CONVERSATION_DB_PATH = os.getenv(
    "CONVERSATION_DB_PATH", os.path.join("..", "conversation_db.sqlite3")
)
EVAL_DB_PATH = os.getenv("EVAL_DB_PATH", os.path.join("..", "eval_db.sqlite3"))
TASK_DB_PATH = os.getenv("TASK_DB_PATH", os.path.join("..", "task_db.sqlite3"))
TASK_OUTPUT_PATH = os.getenv(
    "TASKS_OUTPUT_PATH", os.path.join("..", "local_tasks")
)
REPOSITORY_NAME = os.getenv("REPOSITORY_NAME", "emrgnt-cmplxty/Automata")
MAX_WORKERS = int(os.getenv("MAX_WORKERS", 8))
DATA_ROOT_PATH = os.getenv("DATA_ROOT_PATH", "automata-embedding-data")

GRAPH_TYPE = os.getenv("GRAPH_TYPE", "dynamic")

__all__ = [
    "AgentConfig",
    "LLMProvider",
    "ModelInformation",
    "OpenAIAutomataAgentConfig",
    "OpenAIAutomataAgentConfigBuilder",
]
