# Stage 0 proposal: Recover the stream watermark assigner

Proposed slug: `stream-watermark-assigner`

Category: Software

Subcategory: Data engineering  

Estimated expert time: 7 hours

Out-of-order event shards need event-time watermarks computed with allowed lateness and idle source rules from TOML config. The assigner outputs watermarked event logs and late-data drop reports.

Failed runs exit nonzero without altering a previous successful output set. Verification recomputes watermarks independently, checks idle timeouts, and uses hidden streams with burst lateness beyond allowed slack.

Stream processing time semantics confuse many engineers; explicit contracts make the task fair but still challenging.
