# Software task proposals (50)

Category for all entries: **Software**

Guidelines used: goal first, verifier-visible outcomes only, no step lists, clean-room fixtures, deterministic byte-level grading where appropriate.

---

## 1. Fix the broken job scheduler

**Subcategory:** Systems  
**Expert time:** 6 hours

A batch platform lost its cron-style scheduler after a config migration. The replacement must read a campaign of job definitions, dependency edges, and resource limits, then emit a deterministic execution plan with start times, parallelism groups, and a manifest of skipped or cyclic jobs. The campaign shuffles definition order and uses opaque IDs; nothing in file names reveals priority or grouping.

Verification compares exact plan artifacts against independently recomputed schedules from the same inputs, including hidden campaigns with renamed jobs, tighter resource caps, and dependency cycles that must be rejected without altering a prior successful plan. Staged runs must produce byte-identical outputs when inputs are reshuffled or reordered.

An experienced backend engineer can finish this in one working day because the rules are fully specified in bundled contracts, but the solver still has to infer precedence semantics, cycle detection, and stable tie-breaking from examples rather than from a prose walkthrough.

---

## 2. Rebuild the log rotation tool

**Subcategory:** Systems  
**Expert time:** 5 hours

Operations needs a small utility that rotates application logs under size and age policies without dropping partial lines or breaking active writers. The starter tree contains sample log trees, policy tables, and a stub binary that truncates files incorrectly. The finished tool must produce a rotation report, retained file inventory, and checksum manifest for every run.

The verifier checks line-boundary preservation, gzip naming conventions, idempotent reruns, and failure behavior when a destination is not writable. Hidden fixtures vary timezone stamps, mixed line endings, and concurrent-size edge cases. Outputs must match frozen references byte for byte.

This is a familiar systems task for anyone who has maintained production logs; difficulty comes from getting edge cases and deterministic reporting right, not from obscure algorithms.

---

## 3. Restore the IPC message reassembler

**Subcategory:** Systems  
**Expert time:** 8 hours

A microservice mesh dumped fragmented binary messages across sharded capture files after a broker upgrade. The solver rebuilds a library that joins fragments by session, sequence, and checksum, drops duplicates with stable tie-breaking, and exports ordered message streams plus a gap report. Fragment order and shard names are meaningless.

Verification recomputes joins independently, checks CRC handling, duplicate resolution, and monotonic sequence export. Hidden campaigns introduce torn frames, overlapping sequences, and empty sessions that must fail cleanly. Successful reruns over reshuffled shards must be byte-identical.

The task rewards careful binary parsing and stateful reassembly—common in systems work—but stays bounded because all traps are synthetic and fully documented in the spec bundle.

---

## 4. Repair the systemd unit generator

**Subcategory:** Systems  
**Expert time:** 7 hours

A deployment repo contains service descriptions, environment overlays, and socket units scattered across nested directories, but the generator that merges them into installable unit files was deleted. The solver must rebuild it so that merged units honor override precedence, drop unknown keys, and emit a deterministic bundle plus a diff manifest against the previous generation.

The verifier checks merged unit bytes, precedence rules, invalid key rejection, and preservation of prior output on failure. Hidden trees rename units, add drop-in conflicts, and swap dependency directions. No internet or host-specific paths are involved.

Anyone who has packaged services for Linux can solve this within a day; the challenge is encoding override semantics precisely enough for independent verification.

---

## 5. Recover the cgroups limit applier

**Subcategory:** Systems  
**Expert time:** 9 hours

A container host lost the tool that translates YAML limit profiles into cgroup v2 settings for synthetic workloads. Campaigns supply profile shards, process maps, and worked examples with expected resulting limit files. The rebuilt applier must normalize inputs, resolve conflicts, and write canonical limit artifacts without touching unrelated profiles.

Verification independently derives limit files from the contract formulas, checks conflict failures, and ensures staged regeneration is deterministic across shuffled inputs. Hidden campaigns vary CPU, memory, and IO combinations plus conflicting inheritance rules.

This is realistic capacity-management work compressed into a clean-room exercise; expert time stays moderate because the cgroup mapping is fully specified in bundled JSON schemas.

---

## 6. Reconcile the feature flag rollout state

**Subcategory:** Systems  
**Expert time:** 6 hours

Release engineering stored flag definitions, audience rules, and observed evaluation logs in CSV shards after a partial export. The solver rebuilds a reconciler that computes effective flag states per environment, flags stale definitions, and exports a canonical rollout snapshot. Row and file order carry no meaning.

The verifier recomputes effective states, checks audience matching, stale detection, and byte-identical outputs on reshuffled logs. Hidden fixtures add conflicting rules, empty audiences, and environments missing from the registry that must error without clobbering prior snapshots.

Feature-flag reconciliation is everyday platform work; the task is hard because several independent rules interact and must be graded exactly.

---

## 7. Fix the packet capture indexer

**Subcategory:** Systems  
**Expert time:** 8 hours

Network diagnostics saved pcap slices split across arbitrarily named files. The indexer that builds flow summaries and conversation indexes was corrupted. The solver restores a tool that merges slices, deduplicates by five-tuple and sequence, and writes flow statistics and an index manifest with deterministic ordering.

Verification recomputes flow counts and byte totals from raw packets, validates duplicate handling, and checks hidden captures with overlapping flows and malformed headers that must fail without mutating prior indexes.

Experienced SREs regularly build similar tooling; difficulty is in exact aggregation semantics and stable ordering, not raw data volume.

---

## 8. Restore the temp file cleaner

**Subcategory:** Systems  
**Expert time:** 4 hours

A maintenance daemon should delete expired temp files by inode metadata and path rules, but the current script removes active files. Campaigns include synthetic directory trees, retention policies, and protected path lists. The corrected tool emits a deletion log, retained inventory, and checksum manifest.

The verifier checks that protected and in-use files survive, expired files are removed exactly once, and failed runs leave prior logs untouched. Hidden trees vary mount boundaries, symlink traps, and clock skew encoded in metadata.

This is a short systems hygiene task with enough edge cases to fail naive implementations while remaining solvable in half a day.

---

## 9. Rebuild the SSH authorized-keys merger

**Subcategory:** Systems  
**Expert time:** 5 hours

Identity management exported authorized-keys fragments from several teams in random order. The merger that deduplicates keys, preserves comments, and orders principals lexicographically was lost. The solver rebuilds it to output a canonical keys file and a provenance report listing suppressed duplicates and invalid lines.

Verification parses keys independently, checks OpenSSH formatting, comment preservation, and rejection of malformed entries without altering previous successful merges. Hidden inputs rename principals and include near-duplicate keys with different options.

Standard access-management work; experts can finish quickly because OpenSSH parsing rules are well known, but exact canonical output still requires care.

---

## 10. Repair the rate limiter config compiler

**Subcategory:** Systems  
**Expert time:** 7 hours

An edge proxy reads human-authored limit rules that compile into JSON policy bundles. The compiler was partially overwritten during a refactor. The solver restores compilation of token-bucket and fixed-window rules, including precedence when paths overlap, and emits compiled policy plus diagnostics.

The verifier independently compiles rules, compares bundle bytes, and tests hidden campaigns with overlapping prefixes, zero burst values, and invalid durations that must fail cleanly.

Rate limiting is common infrastructure; the task difficulty is expressing precedence and window math precisely enough for byte-level grading.

---

## 11. Reconstruct the Dijkstra route table exporter

**Subcategory:** Algorithms  
**Expert time:** 6 hours

A network planning tool must read weighted directed graphs from edge list shards, collapse parallel edges by minimum weight, run shortest-path tree construction from a declared root, and export route tables with tie-broken next hops. Shard order and node naming are arbitrary.

Verification recomputes distances and next hops with the same tie rules, checks unreachable node handling, and validates hidden graphs with negative-weight traps that must be rejected. Outputs must be byte-identical across shuffled edge files.

Classic graph algorithms appear in many codebases; an algorithms-minded engineer can implement this in a few hours given explicit tie-breaking contracts.

---

## 12. Restore the interval merge utility

**Subcategory:** Algorithms  
**Expert time:** 4 hours

Calendar sync exported busy intervals from multiple sources as overlapping ranges with inclusive/exclusive boundary conventions mixed together. The utility must normalize boundaries, merge overlaps, subtract exceptions, and write a canonical free-busy timeline. Source order is meaningless.

The verifier recomputes merged intervals, checks boundary semantics, empty results, and invalid range rejection. Hidden fixtures vary timezone-neutral timestamps and nested exceptions.

Interval arithmetic is familiar to backend developers; the task is tricky because boundary conventions must be inferred from examples and enforced exactly.

---

## 13. Fix the topological sort builder

**Subcategory:** Algorithms  
**Expert time:** 5 hours

Build pipelines express task dependencies as shuffled edge lists with optional soft dependencies that may be ignored when flagged. The solver rebuilds a sorter that emits a canonical build order, cycle diagnostics, and a manifest of skipped soft edges. Nothing in node labels reveals layers.

Verification independently topologically sorts with the same soft-edge rules, rejects cycles with stable reporting, and checks byte-identical orders on renamed nodes. Hidden graphs introduce cycle/near-cycle combinations.

Standard CI dependency resolution; experts solve it quickly if they read the soft-edge contract carefully.

---

## 14. Rebuild the LRU cache simulator

**Subcategory:** Algorithms  
**Expert time:** 6 hours

Performance tuning recorded cache access traces as shuffled event shards. The simulator must model a fixed-capacity LRU with explicit tie-breaking on eviction and produce hit/miss statistics plus the final cache state dump. Trace order is not temporal until sorted by the contract clock field.

The verifier replays traces independently, compares statistics and final state bytes, and uses hidden traces with capacity-one edge cases and duplicate timestamps.

Cache simulation is textbook material made practical; difficulty is deterministic replay semantics, not algorithm novelty.

---

## 15. Recover the string suffix array builder

**Subcategory:** Algorithms  
**Expert time:** 8 hours

Bioinformatics tooling indexed synthetic reference strings split across fragments with duplicated substrings. The suffix array builder must concatenate fragments in manifest order, build a suffix array with stable lexicographic tie rules, and export rank tables. Fragment names are decoys.

Verification recomputes suffix arrays for moderate-length strings, checks rank invariants, and tests hidden references with repeated motifs. Memory limits fit the stated resource envelope using standard library structures only.

Experienced engineers who have worked with indexing can finish in a day; the task tests careful string handling rather than research-grade suffix array theory.

---

## 16. Restore the convex hull exporter

**Subcategory:** Algorithms  
**Expert time:** 7 hours

A CAD preprocessor collected 2-D point clouds from CSV shards with duplicate and collinear points. The hull builder must deduplicate by contract rules, emit vertices in counterclockwise order starting from the lowest-left point, and write area and perimeter as reduced fractions.

The verifier recomputes hulls independently, checks collinear handling, empty inputs, and hidden clouds with many duplicates on one line.

Computational geometry basics; experts can implement Graham scan or monotone chain within hours given exact tie rules in the spec.

---

## 17. Fix the meeting room scheduler

**Subcategory:** Algorithms  
**Expert time:** 5 hours

Facilities management exported room booking requests as shuffled intervals with priorities and room capabilities. The scheduler assigns rooms to maximize covered high-priority minutes under non-overlap constraints with deterministic tie-breaking when choices tie.

Verification recomputes assignments independently, checks capability filtering, unassigned request reporting, and hidden request sets with equal-priority conflicts.

Classic interval scheduling with extra constraints; solvable in an afternoon with clear scoring rules.

---

## 18. Rebuild the edit distance batch matcher

**Subcategory:** Algorithms  
**Expert time:** 6 hours

Data quality tooling compares identifier lists from two shuffled CSV shards and must pair rows by minimum Levenshtein distance with deterministic tie-breaking when distances collide. The tool exports pairings, unmatched rows, and a summary manifest.

The verifier recomputes distances with the contract cost model, validates tie rules, and tests hidden lists with many equidistant candidates.

Dynamic programming at small scale; experts know the algorithm—the work is encoding ties and unmatched handling exactly.

---

## 19. Repair the union-find connectivity reporter

**Subcategory:** Algorithms  
**Expert time:** 5 hours

Incident response grouped hosts into connectivity components from undirected edge shards with lexicographic component IDs required in output. The union-find implementation must use union-by-rank and path compression while still emitting components in the contract’s canonical order.

Verification rebuilds components independently, checks canonical IDs, rejects self-loops where forbidden, and validates hidden graphs with star and chain topologies.

Standard disjoint-set work; moderate difficulty comes from output ordering requirements, not from the core algorithm.

---

## 20. Restore the regex token parser

**Subcategory:** Algorithms  
**Expert time:** 8 hours

A small pattern matcher supports a documented subset of regex syntax for log filtering. Its tokenizer and postfix converter were lost. The solver rebuilds parsing to emit token streams and syntax trees for valid patterns, with precise error locations for invalid ones.

The verifier compares token and tree bytes for visible and hidden patterns, including nested groups, escaped literals, and empty alternations that must fail. No full engine is required—only parse artifacts.

Parsing tasks reward careful grammar handling; an expert compiler-adjacent engineer can finish within a day given the bundled grammar tables.

---

## 21. Reconcile the migration journal

**Subcategory:** Databases  
**Expert time:** 10 hours

A Postgres-style migration runner crashed mid-deploy, leaving SQL journals, applied markers, and pending scripts in inconsistent shards. The solver rebuilds a reconciler that computes the exact apply order, detects split-brain markers, and exports a recovery plan plus normalized journal state. File order is arbitrary.

Verification independently derives apply order from markers, checks idempotency tokens, rejects conflicting checksums, and ensures failed analysis does not mutate prior successful exports. Hidden campaigns rename scripts and include forked marker histories.

Database operators handle this class of problem regularly; difficulty is multi-file consistency rather than exotic SQL.

---

## 22. Fix the B-tree page validator

**Subcategory:** Databases  
**Expert time:** 9 hours

An educational storage engine stores synthetic B-tree pages as binary shards. The validator must verify key order, child pointers, occupancy bounds, and free space accounting, then export a validation report and flattened key listing. Page order in the campaign is shuffled.

The verifier recomputes structural invariants independently, checks underflow detection, and tests hidden trees with intentional pointer corruption that must fail without altering prior reports.

Index structure validation is core database internals work; experts with storage background can complete it in about a day given explicit page layouts.

---

## 23. Restore the query plan serializer

**Subcategory:** Databases  
**Expert time:** 8 hours

An optimizer emits intermediate plan trees as JSON fragments split across files. The serializer must merge fragments, resolve node IDs, topologically sort operators, and write a canonical plan document plus cost summary using rational arithmetic from the contract.

Verification rebuilds plans from fragments, compares serialized bytes, and uses hidden plans with duplicate IDs and missing roots that must error cleanly.

Query-plan tooling is familiar to database engineers; challenge lies in canonical JSON and ID resolution rules.

---

## 24. Rebuild the WAL segment compactor

**Subcategory:** Databases  
**Expert time:** 11 hours

Append-only WAL segments with checksum frames must be compacted by dropping superseded records and tombstones while preserving commit order. The compactor reads sharded segment files and writes compacted segments plus a manifest of dropped ranges.

The verifier independently replays and compacts, checks CRC validation, sequence monotonicity, and byte-identical compactions on reshuffled inputs. Hidden segments include torn frames and duplicate LSNs.

WAL compaction mirrors real database maintenance; long horizon comes from staged correctness, not huge files.

---

## 25. Repair the index diff tool

**Subcategory:** Databases  
**Expert time:** 7 hours

Two index snapshots from synthetic tables arrive as sorted key dumps in CSV shards. The diff tool must emit added, removed, and changed keys with old/new values, using deterministic ordering independent of shard names.

Verification recomputes diffs independently, checks value equality semantics, and tests hidden snapshots with reorder-only shards that must not appear as changes.

Table diffing is routine; exact output formatting and stable ordering make it suitable for automated grading.

---

## 26. Recover the connection pool balancer

**Subcategory:** Databases  
**Expert time:** 6 hours

A pool manager assigns database connections to waiting clients under max pool size, idle timeouts, and fairness rules documented in TOML campaigns. The solver rebuilds the allocator to produce assignment traces and final pool state dumps for each replay.

The verifier replays request logs independently, checks fairness tie-breaking, timeout eviction, and hidden logs with burst traffic and zero pool size errors.

Connection pooling is everyday backend work; the task tests precise replay semantics.

---

## 27. Fix the schema registry validator

**Subcategory:** Databases  
**Expert time:** 8 hours

Avro-like schema versions are stored as shuffled JSON documents with compatibility rules. The validator must check backward/forward compatibility, emit violation reports, and write a canonical registry snapshot sorted by subject and version.

Verification applies compatibility rules independently, checks transitive violations, and uses hidden registries with enum reorder traps.

Schema evolution is common in event-driven systems; experts can implement compatibility checks within a day using bundled rules.

---

## 28. Restore the materialized view refresher

**Subcategory:** Databases  
**Expert time:** 9 hours

Materialized view definitions and change feeds arrive as CSV shards. The refresher computes incremental updates using timestamp windows and primary-key upserts, then exports refreshed view rows and a refresh manifest. Feed order is meaningless until normalized.

The verifier recomputes view contents independently, checks window boundaries, duplicate keys, and hidden feeds with out-of-order timestamps.

Incremental view maintenance is realistic warehouse work; difficulty is combining normalization, upsert semantics, and deterministic export.

---

## 29. Reconcile the deadlock wait graph

**Subcategory:** Databases  
**Expert time:** 7 hours

Transaction waits were captured as edge lists between synthetic transactions with lock modes. The tool must build a wait-for graph, detect cycles, propose victim transactions by contract tie rules, and export a resolution trace.

Verification rebuilds graphs and victim choices independently and tests hidden waits with multiple equal-cost victims requiring lexicographic choice.

Deadlock detection is taught in database courses; applying explicit victim tie rules makes it gradable.

---

## 30. Rebuild the CSV-to-Parquet column mapper

**Subcategory:** Data engineering  
**Expert time:** 8 hours

A pipeline should map loosely typed CSV shards into a fixed column schema with type coercion, null sentinels, and rational rounding for numeric fields. The mapper was lost during a platform move. Outputs include normalized rows, rejected row reports, and a schema conformance manifest.

The verifier recomputes coercions and rounding independently, checks null handling, and uses hidden shards with conflicting type hints and overflow values that must fail without clobbering prior outputs.

ETL coercion rules are daily data-engineering work; byte-exact manifests make naive shortcuts fail.

---

## 31. Fix the incremental deduplication job

**Subcategory:** Data engineering  
**Expert time:** 7 hours

Streaming dedup state and new event shards must be merged so duplicates collapse by business key with earliest-seen wins unless a tombstone marker says otherwise. The job exports updated state, accepted events, and duplicate statistics.

Verification replays merges independently, checks tombstone precedence, and tests hidden shards with reshuffled duplicates and partial state files.

Dedup pipelines are common; difficulty is stable merge semantics across stages.

---

## 32. Restore the partition assignment planner

**Subcategory:** Data engineering  
**Expert time:** 6 hours

Kafka-style topics arrive with partition counts, key hash rules, and consumer group members. The planner assigns partitions to members for balanced load with deterministic tie-breaking when weights equal.

The verifier recomputes assignments independently, checks balance metrics, unknown topic rejection, and hidden groups with uneven member capacities.

Partition assignment is familiar to streaming engineers; the task is bounded and fully synthetic.

---

## 33. Rebuild the data quality rules engine

**Subcategory:** Data engineering  
**Expert time:** 9 hours

Quality rules expressed in a small DSL must run over shuffled row batches, emitting violation records with row keys and rule IDs sorted canonically. The engine parses rules, evaluates predicates with null semantics from the contract, and writes summary counts.

Verification evaluates rules independently, compares violation bytes, and uses hidden batches with borderline null comparisons and conflicting rule priorities.

Rule engines appear in every warehouse; parsing plus null semantics supplies enough depth for a day’s work.

---

## 34. Recover the slow-changing dimension merger

**Subcategory:** Data engineering  
**Expert time:** 10 hours

SCD type-2 history for synthetic customers lives in CSV shards with overlapping effective dates. The merger must close and open rows by contract rules, collapse exact duplicates, and export current and historical tables plus a change manifest.

The verifier recomputes histories independently, checks date boundary semantics, and tests hidden inputs with overlapping intervals that must error.

Dimensional modeling is standard BI work; experts know the patterns—precision in date logic is what makes it hard.

---

## 35. Fix the metric rollup compiler

**Subcategory:** Data engineering  
**Expert time:** 7 hours

Raw counter shards must roll up to hourly and daily aggregates using explicit timezone-neutral bucketing and max/last/sum policies per metric name. The compiler writes rollup tables and a policy manifest.

Verification recomputes buckets independently, checks policy selection, and validates hidden metrics with irregular sampling intervals.

Metrics rollups are everyday observability tasks; graders focus on bucket boundaries and policy maps.

---

## 36. Restore the schema evolution applier

**Subcategory:** Data engineering  
**Expert time:** 8 hours

Event streams ship with embedded schema version markers and companion evolution scripts. The applier must choose the correct script chain, upgrade row shapes, and export upgraded events plus an evolution log. Order of files is decoy data.

The verifier replays evolution independently, checks incompatible skips, and uses hidden streams requiring multi-hop upgrades.

Schema evolution pipelines reward careful versioning; synthetic fixtures keep the task self-contained.

---

## 37. Rebuild the fuzzy join matcher

**Subcategory:** Data engineering  
**Expert time:** 9 hours

Two shuffled entity tables must join on composite keys with optional phonetic normalization rules from the contract. The matcher exports paired rows, unmatched lists, and similarity scores as reduced fractions.

Verification recomputes joins and scores independently, checks normalization tables, and tests hidden tables with symmetric ties broken lexicographically.

Record linkage shows up in real pipelines; difficulty is exact normalization and tie-breaking, not ML.

---

## 38. Repair the checkpoint manifest validator

**Subcategory:** Data engineering  
**Expert time:** 6 hours

Spark-style job checkpoints list partial RDD manifests across shards. The validator verifies hash chains, missing parts, and lineage completeness, then exports a consolidated manifest or a structured error report.

The verifier rebuilds hash chains independently, detects broken lineage, and ensures failed validation preserves prior good manifests.

Checkpoint validation is practical batch-processing hygiene; experts can finish in an afternoon.

---

## 39. Recover the stream watermark assigner

**Subcategory:** Data engineering  
**Expert time:** 7 hours

Out-of-order event shards need event-time watermarks computed with allowed lateness and idle source rules from TOML config. The assigner outputs watermarked event logs and late-data drop reports.

Verification recomputes watermarks independently, checks idle timeouts, and uses hidden streams with burst lateness beyond allowed slack.

Stream processing time semantics confuse many engineers; explicit contracts make the task fair but still challenging.

---

## 40. Fix the HTML form accessibility report

**Subcategory:** Frontend  
**Expert time:** 5 hours

A static multi-page form bundle ships without its accessibility checker. The tool must parse HTML fragments, evaluate label associations, tabindex order, and ARIA role rules from the bundled spec, and export violation lists with line references.

The verifier compares violation sets independently, checks hidden pages with duplicate IDs and missing labels, and rejects malformed HTML without altering prior reports.

Frontend engineers regularly run a11y audits; this packages common checks into deterministic output.

---

## 41. Restore the CSS bundle optimizer

**Subcategory:** Frontend  
**Expert time:** 6 hours

Stylesheets arrive as shuffled partials with variables and imports. The optimizer must flatten imports, resolve custom properties, deduplicate selectors by contract precedence, and emit a canonical CSS file plus an unused-rule report.

Verification recomputes flattened CSS bytes independently, checks import cycles that must fail, and tests hidden partials with conflicting custom properties.

Build-tool authors know this problem; graders enforce precedence exactly so shortcuts fail.

---

## 42. Rebuild the component prop validator

**Subcategory:** Frontend  
**Expert time:** 7 hours

A design system ships JSON component schemas and example usage files. The validator checks required props, enum values, and mutually exclusive prop groups, exporting diagnostics sorted by component and prop name.

The verifier evaluates schemas independently, checks hidden examples with subtle mutual exclusion violations, and ensures failed runs do not mutate prior diagnostics.

Design-system tooling is common in frontend platform teams; difficulty is exhaustive rule coverage, not UI rendering.

---

## 43. Fix the sitemap generator

**Subcategory:** Frontend  
**Expert time:** 4 hours

Marketing sites store route metadata in YAML shards with changefreq and priority fields. The generator must merge shards, resolve canonical URLs, drop duplicates by path, and write a sorted sitemap XML file plus a collision report.

Verification recomputes XML bytes independently, checks URL normalization, and tests hidden shards with trailing-slash conflicts.

Simple but real frontend infra; experts finish quickly if URL normalization rules are followed precisely.

---

## 44. Recover the markdown static site builder

**Subcategory:** Frontend  
**Expert time:** 8 hours

Markdown posts and layout templates must compile into HTML pages with front matter parsing, relative link rewriting, and deterministic asset hashing. The builder was partially deleted.

The verifier compares generated HTML bytes, checks link targets, missing template errors, and hidden posts with ambiguous front matter keys.

Static site generators are familiar; challenge is canonical HTML and link rewriting without a browser.

---

## 45. Repair the design token compiler

**Subcategory:** Frontend  
**Expert time:** 6 hours

Design tokens live in JSON with alias references and math expressions using rational numbers. The compiler resolves aliases, evaluates expressions, and exports flattened token files for color, spacing, and typography scales.

Verification recomputes token values independently, detects alias cycles, and uses hidden tokens with division rounding traps.

Design ops teams use token pipelines; exact rational math makes naive float shortcuts fail grading.

---

## 46. Restore the JSX import graph linter

**Subcategory:** Frontend  
**Expert time:** 7 hours

A monorepo exports a shuffled list of synthetic JSX modules with import statements. The linter must detect unused imports, circular dependencies, and forbidden cross-package imports per a rules table, exporting violations in canonical order.

The verifier rebuilds import graphs independently and tests hidden modules with re-export cycles and alias paths.

Frontend platform linting is everyday work; graph analysis supplies enough depth for automated verification.

---

## 47. Fix the service worker cache manifest

**Subcategory:** Frontend  
**Expert time:** 5 hours

PWA assets are listed in JSON shards with cache busting hashes and route patterns. The manifest builder merges shards, applies pattern specificity rules, and writes a canonical precache list.

Verification recomputes merge results independently, checks specificity ties, and validates hidden shards with overlapping patterns.

Progressive web app caching is practical frontend systems work with clear gradable outputs.

---

## 48. Rebuild the INI configuration parser

**Subcategory:** Languages  
**Expert time:** 6 hours

Services still load INI files with nested sections, continuation lines, and quoted values. The parser must emit a canonical JSON representation with stable key ordering and precise error locations for invalid input.

The verifier compares JSON bytes for visible and hidden INI files, including duplicate keys, invalid escapes, and mixed line endings.

Config parsers are language-tooling bread and butter; experts can implement one in hours given explicit grammar notes.

---

## 49. Restore the expression evaluator

**Subcategory:** Languages  
**Expert time:** 8 hours

A spreadsheet-like language supports integers, rationals, variables, and nested functions listed in the contract. The evaluator must parse expressions, resolve variables from environment shards, and export reduced rational results plus AST dumps.

Verification recomputes evaluations independently, checks divide-by-zero failures, and tests hidden expressions with variable shadowing.

Small language implementations are common interview and tooling tasks; AST and rational output make grading objective.

---

## 50. Fix the bytecode disassembler

**Subcategory:** Languages  
**Expert time:** 9 hours

A teaching VM ships synthetic bytecode files with opcodes documented in a table. The disassembler must decode instructions, resolve jump targets, and write human-readable listings with stable label names derived by contract rules—not by discovery order.

The verifier compares listing bytes independently, checks jump alignment, unknown opcode rejection, and hidden programs with overlapping jump tables.

VM tooling is classic languages work; experts with interpreter experience can finish within a day using the opcode spec alone.
