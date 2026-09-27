"""Run in the terminal.
  uv run energy-agent "Which month had the highest average price?"
  uv run energy-agent --thread my-analysis          (chat; continue later with the same name)"""
import argparse
import logging

from energy_agent.agent import ask, build_agent, get_checkpointer
from energy_agent.app import build_toolbox


def main() -> None:
    parser = argparse.ArgumentParser(description="Energy-market analyst agent")
    parser.add_argument("question", nargs="*", help="question (leave empty for chat mode)")
    parser.add_argument("--thread", default="default", help="conversation name; reuse it to continue")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="  %(message)s")
    agent = build_agent(build_toolbox().as_langchain_tools(), checkpointer=get_checkpointer())

    if args.question:
        print(ask(agent, " ".join(args.question), args.thread))
        return
    print(f"Chat mode, thread '{args.thread}'. Empty line to quit.")
    while q := input("\nYou: ").strip():
        print("Agent:", ask(agent, q, args.thread))


if __name__ == "__main__":
    main()
