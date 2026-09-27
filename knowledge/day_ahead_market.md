# The day-ahead market and the merit order

Short notes written for this project. Check details at smard.de.

On the day-ahead market, electricity for delivery on the next day is traded in a daily auction held
the day before. European markets are coupled, so the auction also allocates cross-border capacity.

The price is set by the merit order: all sell offers are sorted from cheapest to most expensive, and the
most expensive offer still needed to cover demand sets the price for everyone in that period. Renewables
with near-zero running costs sit at the start of the merit order; gas plants are often at the end and set
the price when demand is high or wind and solar output is low.

Historically the day-ahead market traded hourly products. In 2025 the European day-ahead market moved to
15-minute products, so check which resolution a SMARD export uses before comparing periods.
