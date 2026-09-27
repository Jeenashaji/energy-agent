"""CONCEPT: tools.
Plain Python functions the agent is allowed to call. The docstring is what the
LLM reads to decide when to use a tool, so it is written for the model.
The same Toolbox is used by the LangChain agent AND the MCP server."""
import duckdb
import pandas as pd
from langchain.tools import tool
from langchain_core.vectorstores import VectorStore

from energy_agent.config import MAX_ROWS, TOP_K_DOCS


class Toolbox:
    def __init__(self, df: pd.DataFrame, con: duckdb.DuckDBPyConnection, docs: VectorStore):
        self.df, self.con, self.docs = df, con, docs

    def describe_data(self) -> str:
        """List the SQL table name, columns, types, time range and row count. Call this before writing SQL."""
        cols = ", ".join(f"{c} ({t})" for c, t in zip(self.df.columns, self.df.dtypes.astype(str)))
        return (f"Table 'data' with {len(self.df)} rows, from {self.df.ts.min()} to {self.df.ts.max()}.\n"
                f"Columns: {cols}. Prices are in EUR/MWh.")

    def run_sql(self, query: str) -> str:
        """Run a read-only DuckDB SQL query on table 'data'. Use it for every number you report.
        Aggregate (AVG, MAX, COUNT, GROUP BY) instead of selecting raw rows."""
        if not query.strip().lower().startswith(("select", "with")):   # guardrail: read-only
            return "Error: only SELECT / WITH queries are allowed."
        try:
            result = self.con.execute(query).df()
        except Exception as e:          # the agent sees the error and can fix its own query
            return f"SQL error: {e}"
        note = f"\n(showing first {MAX_ROWS} of {len(result)} rows)" if len(result) > MAX_ROWS else ""
        return result.head(MAX_ROWS).to_string(index=False) + note

    def search_docs(self, question: str) -> str:
        """Search the knowledge base for background explanations (market rules, why prices go
        negative, what the data columns mean). Use it for 'why' / 'what is' questions, not for numbers."""
        hits = self.docs.similarity_search(question, k=TOP_K_DOCS)
        return "\n\n".join(f"[{h.metadata['source']}] {h.page_content}" for h in hits)

    def as_langchain_tools(self) -> list:
        return [tool(self.describe_data), tool(self.run_sql), tool(self.search_docs)]
