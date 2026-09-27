from energy_agent.data import load_smard_csv
from tests.conftest import SAMPLE


def test_german_number_format_is_parsed():
    df = load_smard_csv(SAMPLE)
    assert list(df.columns) == ["ts", "deutschland_luxemburg", "belgien"]
    assert df.deutschland_luxemburg.iloc[1] == 1308.97   # "1.308,97"
    assert df.deutschland_luxemburg.iloc[2] == -5.5      # negative price
    assert df.deutschland_luxemburg.isna().iloc[3]       # "-" means missing
