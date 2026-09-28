# Ledgerkit API contract

Java 21 and the standard library are the only runtime requirements.

## Command line

Each command takes `CAMPAIGN OUTPUT`:

```text
java -cp /app ledgerkit.Main ingest CAMPAIGN OUTPUT
java -cp /app ledgerkit.Main normalize CAMPAIGN OUTPUT
java -cp /app ledgerkit.Main match CAMPAIGN OUTPUT
java -cp /app ledgerkit.Main settle CAMPAIGN OUTPUT
java -cp /app ledgerkit.Main round CAMPAIGN OUTPUT
java -cp /app ledgerkit.Main reconcile CAMPAIGN OUTPUT
java -cp /app ledgerkit.Main export CAMPAIGN OUTPUT
java -cp /app ledgerkit.Main run CAMPAIGN OUTPUT
```

`ingest` reads all campaign definitions and ledger and settlement shards. Later commands read
definitions plus only their declared artifacts in `output-schema.json`; they
must not enumerate or read `CAMPAIGN/ledger` or `CAMPAIGN/settlements`. `run` executes the same public
stage functions in order in a temporary output directory, then atomically
replaces all nine products. Commands return zero on success and nonzero after
printing one concise error to stderr on failure.

## Public Java API

`ledgerkit.Pipeline` exposes static methods:

```java
void ingest(String campaign, String output);
void normalize(String campaign, String output);
void match(String campaign, String output);
void settle(String campaign, String output);
void round(String campaign, String output);
void reconcile(String campaign, String output);
void exportStage(String campaign, String output);
void run(String campaign, String output);
```

`ledgerkit.Exact.roundHalfAway(long numerator, long denominator)` accepts a
positive integer denominator and returns the nearest integer with ties rounded
away from zero.

## Campaign files

`campaign.toml` contains `schema_version`, `base_currency`,
`settlement_lag_business_days`, and `business_calendar` as a JSON array string
of ISO `YYYY-MM-DD` holiday dates.

CSV schemas are exact:

* `currencies.csv`: `currency_code,exponent`
* `fx_rates.csv`: `as_of_date,from_currency,to_currency,numerator,denominator`
* `accounts.csv`: `account_id,currency,name`
* each `ledger/*.csv`: `entry_id,account_id,trade_date,amount_minor,currency,side`
* each `settlements/*.csv`: `batch_id,line_id,entry_ref,trade_date,settle_date,gross_minor,fee_minor,currency,status`
* `reversals.csv`: `reversal_id,batch_id,line_id,reversal_date,amount_minor,currency`

Identifiers are nonempty printable ASCII without leading or trailing whitespace.
All dates are canonical ISO `YYYY-MM-DD`. Amounts are signed integer minor units
after normalization: `DR` is positive, `CR` is negative. Settlement `gross_minor`
may be negative for credit/refund lines. FX rates convert from `from_currency`
to `base_currency`. Only `posted` settlements contribute to settlement totals.
Partial reversals subtract `amount_minor` from the linked settlement line net
and from the linked ledger entry effective amount.

Expected settlement date is `trade_date` plus `settlement_lag_business_days`
business days, skipping Saturday, Sunday, and `business_calendar` holidays.
`drift_business_days` is the signed business-day count from expected to reported
settle date.

Base conversion for a native minor amount uses the latest FX rate with
`as_of_date <= trade_date`:

`base_minor = roundHalfAway(signed_native * numerator * 10^base_exponent, denominator * 10^from_exponent)`

## Canonical products

JSON is UTF-8, sort-key ordered, indented by two spaces, and LF terminated.
JSONL is compact sort-key ordered JSON, one object per LF-terminated line.
Array ordering and JSONL ordering are semantic and are specified by the output
schema. No product contains absolute paths, wall-clock times, shard names, row
numbers, random values, or platform-dependent data.

`reconciliation.json` contains an `accounts` array and `all_tied`. Each account
row reports `ledger_base_total`, `settlement_base_total`, and `tied`.
`exceptions.jsonl` records `unmatched_settlement`, `unmatched_entry`,
`settle_drift`, and `account_imbalance` rows with the fields produced by the
reference contract.
