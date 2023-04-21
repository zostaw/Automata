import argparse
import logging
import logging.config

from termcolor import colored

from spork.agents.agent_configs.agent_version import AgentVersion
from spork.agents.mr_meeseeks_agent import MrMeeseeksAgent
from spork.tools.python_tools.python_indexer import PythonIndexer
from spork.tools.tool_managers.tool_utils import load_llm_tools
from spork.tools.utils import get_logging_config, root_py_path


def main():
    parser = argparse.ArgumentParser(description="Run the MrMeeseeksAgent.")
    parser.add_argument("--instructions", type=str, help="The initial instructions for the agent.")
    parser.add_argument(
        "--version",
        type=AgentVersion,
        default=AgentVersion.MEESEEKS_MASTER_V1,
        help="The version of the agent.",
    )
    parser.add_argument(
        "--model", type=str, default="gpt-4", help="The model to be used for the agent."
    )
    parser.add_argument(
        "--documentation_url",
        type=str,
        default="https://python.langchain.com/en/latest",
        help="The model to be used for the agent.",
    )
    parser.add_argument(
        "--session_id", type=str, default=None, help="The session id for the agent."
    )
    parser.add_argument(
        "--stream", type=bool, default=True, help="Should we stream the responses?"
    )
    parser.add_argument(
        "--tools",
        type=str,
        default="python_indexer,python_writer,codebase_oracle",
        help="Comma-separated list of tools to be used.",
    )

    parser.add_argument("-v", "--verbose", action="store_true", help="increase output verbosity")

    args = parser.parse_args()

    logging_config = get_logging_config(log_level=logging.DEBUG if args.verbose else logging.INFO)
    logging.config.dictConfig(logging_config)
    logger = logging.getLogger(__name__)

    requests_logger = logging.getLogger("urllib3")

    # Set the logging level for the requests logger to WARNING
    requests_logger.setLevel(logging.INFO)
    openai_logger = logging.getLogger("openai")
    openai_logger.setLevel(logging.INFO)

    assert not (
        args.instructions is None and args.session_id is None
    ), "You must provide instructions for the agent if you are not providing a session_id."
    assert not (
        args.instructions and args.session_id
    ), "You must provide either instructions for the agent or a session_id."

    inputs = {"documentation_url": args.documentation_url, "model": args.model}
    _, exec_tools = load_llm_tools(args.tools.split(","), inputs, logger)
    indexer = PythonIndexer(root_py_path())

    initial_payload = {
        "overview": indexer.get_overview(),
    }

    logger.info("Passing in instructions:\n%s", colored(args.instructions, "magenta"))
    logger.info("-" * 60)
    agent = MrMeeseeksAgent(
        initial_payload=initial_payload,
        instructions=args.instructions,
        tools=exec_tools,
        version=args.version,
        model=args.model,
        session_id=args.session_id,
        stream=args.stream,
    )

    logger.info("Running the agent now...")
    if args.session_id is None:
        agent.run()
    else:
        logger.info("Replaying messages...")
        agent.replay_messages()

    while True:
        user_input = input(
            "Do you have any further instructions or feedback? Type 'exit' to terminate: "
        )
        if user_input.lower() == "exit":
            break
        else:
            instructions = [{"role": "user", "content": user_input}]
            agent.extend_last_instructions(instructions)
            agent.iter_task()


if __name__ == "__main__":
    main()
