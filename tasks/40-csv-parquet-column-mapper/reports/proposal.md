# Stage 0 proposal: Rebuild the CSV-to-Parquet column mapper

Proposed slug: `csv-parquet-column-mapper`

Category: Software

Subcategory: Data engineering  

Estimated expert time: 8 hours

A pipeline should map loosely typed CSV shards into a fixed column schema with type coercion, null sentinels, and rational rounding for numeric fields. The mapper was lost during a platform move. Outputs include normalized rows, rejected row reports, and a schema conformance manifest.

The verifier recomputes coercions and rounding independently, checks null handling, and uses hidden shards with conflicting type hints and overflow values that must fail without clobbering prior outputs.

ETL coercion rules are daily data-engineering work; byte-exact manifests make naive shortcuts fail.
