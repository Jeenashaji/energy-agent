# SMARD data: what the columns mean

Short notes written for this project. Check details at smard.de.

SMARD is the electricity-market data platform of the Bundesnetzagentur (German Federal Network Agency).
It publishes generation, consumption, cross-border flows and wholesale prices for Germany.

The wholesale price export contains day-ahead prices per bidding zone in EUR/MWh.
The column "Deutschland/Luxemburg" is the German-Luxembourg bidding zone (DE-LU), which has been a
single price zone since 1 October 2018, when it was separated from Austria.
Other columns are neighbouring bidding zones, for example Belgium or the Netherlands.

Timestamps are the start of each delivery period in German local time. A value of "-" means no price
was published for that period.
