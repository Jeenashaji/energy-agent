"""CONCEPT: evaluation. Ask every question in questions.csv and grade the answers.
Fill the 'expected' column first (compute the numbers yourself in notebook 01).
  uv run python evals/run_evals.py"""
import csv
import re
from pathlib import Path

HERE = Path(__file__).parent


def numbers_in(text: str) -> list[float]:
    return [float(x.replace(",", "")) for x in re.findall(r"-?\d[\d,]*\.?\d*", text)]


def grade(answer: str, expected: str) -> str:
    """Number expected -> any number in the answer within 1%. Text expected -> must appear in answer."""
    if not expected.strip():
        return "not graded"
    try:
        target = float(expected)
        ok = any(abs(n - target) <= max(0.01, abs(target) * 0.01) for n in numbers_in(answer))
    except ValueError:
        ok = expected.lower() in answer.lower()
    return "pass" if ok else "FAIL"


def main() -> None:
    from energy_agent.agent import ask, build_agent
    from energy_agent.app import build_toolbox

    agent = build_agent(build_toolbox().as_langchain_tools())   # no memory: each question independent
    rows = list(csv.DictReader(open(HERE / "questions.csv", encoding="utf-8")))
    for row in rows:
        row["answer"] = ask(agent, row["question"])
        row["result"] = grade(row["answer"], row["expected"])
        print(f"[{row['result']}] {row['question']}\n   {row['answer']}\n")
    with open(HERE / "results.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    graded = [r for r in rows if r["result"] != "not graded"]
    print(f"Score: {sum(r['result'] == 'pass' for r in graded)}/{len(graded)} graded questions passed")


if __name__ == "__main__":
    main()
