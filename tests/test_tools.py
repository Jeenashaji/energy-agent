def test_describe_data(toolbox):
    assert "deutschland_luxemburg" in toolbox.describe_data()


def test_sql_returns_numbers(toolbox):
    out = toolbox.run_sql("SELECT count(*) AS n FROM data WHERE deutschland_luxemburg < 0")
    assert "1" in out


def test_write_queries_are_blocked(toolbox):
    assert toolbox.run_sql("DROP TABLE data").startswith("Error")


def test_sql_errors_are_returned_not_raised(toolbox):
    assert toolbox.run_sql("SELECT missing_column FROM data").startswith("SQL error")


def test_langchain_tools_have_names(toolbox):
    assert [t.name for t in toolbox.as_langchain_tools()] == ["describe_data", "run_sql", "search_docs"]
