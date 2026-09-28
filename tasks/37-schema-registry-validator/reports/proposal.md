# Stage 0 proposal: Fix the schema registry validator

Proposed slug: `schema-registry-validator`

Category: Software

Subcategory: Databases  

Estimated expert time: 8 hours

Avro-like schema versions are stored as shuffled JSON documents with compatibility rules. The validator must check backward/forward compatibility, emit violation reports, and write a canonical registry snapshot sorted by subject and version.

Failed runs exit nonzero without altering a previous successful output set. Verification applies compatibility rules independently, checks transitive violations, and uses hidden registries with enum reorder traps.

Schema evolution is common in event-driven systems; experts can implement compatibility checks within a day using bundled rules.
