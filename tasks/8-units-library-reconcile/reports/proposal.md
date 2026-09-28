# Stage 0 proposal: Units Library Reconcile

Proposed slug: `units-library-reconcile`

Category: Science

Implementation language: Java 21 standard library

Estimated expert time: 12–16 hours

A multi-source measurement campaign used a dimensional-analysis library to merge
observations from several instruments. The library lost conversion stages during
a migration, and two data sources spell the same physical units differently.
Merged series fail conservation checks when alias conventions are ignored.

The task is to rebuild the lost unit library package. The supplied campaign
contains a unit registry CSV, conservation rules, and shuffled CSV shards of
observations. Each row carries a magnitude and unit symbol. Shard names and row
order carry no source or convention meaning.

The solution begins by loading and validating the campaign. Exact duplicate rows
are collapsed, conflicting identifiers are rejected, and all observations are
normalized into a deterministic form.

Unit strings are parsed against the registry, including alias groups that map
`lbf`/`lb_f` and `cal`/`calorie` style spellings to canonical symbols. A
conversion graph is built from registry factors and offsets using exact rational
arithmetic.

Each observation is converted to SI magnitudes, merged by quantity and
timestamp, and checked against the conservation constraints. A source that uses
the wrong alias convention produces plausible per-row values yet fails the
conservation report on the merged series.

The implementation emits independently graded products for normalized input,
parsed units, the conversion graph, converted observations, the convention map,
merged series, conservation report, rejections, and provenance. Staged and
complete runs must be byte-identical.

The task is clean-room: registries, datasets, alias traps, and expected outputs
are generated specifically for this project. Visible campaigns demonstrate every
rule; hidden campaigns rename, resize, and recombine those behaviors, including
swapped alias conventions across sources.

The long horizon comes from seven dependent stages—strict ingestion, unit
parsing, conversion-graph construction, SI conversion, series merge,
conservation validation, and canonical export—rather than from oversized
fixtures or undocumented edge cases.

Success requires three deterministic Oracle rewards of 1.0, NOP and adversarial
rewards of 0.0, a clean Harbor/TB4 package, and an official Stage 2 median
above 80 assistant turns.
