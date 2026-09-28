# Stage 0 proposal: CTD Cast Processing

Proposed slug: `ctd-cast-processing`

Category: Science

Implementation language: Python standard library

Estimated expert time: 12–16 hours

A CTD cast records conductivity, temperature, and pressure while a probe descends
and ascends through the water column. The downcast carries the primary science
profile; the upcast is discarded. Depth is recovered from pressure using a
latitude-dependent gravity formula, and density is derived from salinity,
temperature, and pressure using simplified UNESCO-style rational coefficients.

The task is to rebuild the lost processing package. The supplied campaign
contains a cast header with latitude and bin size, and shuffled CSV shards of
profile rows. Row order and filenames carry no downcast meaning.

The solution begins by loading and validating the campaign. Exact duplicate rows
are collapsed, conflicting identifiers are rejected, and all samples are
normalized into a deterministic form.

The downcast is the longest time-ordered prefix whose pressures are
non-decreasing and reach the campaign maximum. The upcast is discarded.

Pressure is converted to depth with exact rational arithmetic using the header
latitude, salinity is derived from conductivity and temperature, and density is
computed from the contract equation. Samples are averaged into depth bins.

The cast header latitude may lie. Candidate latitudes from the header and
campaign list are scored by density inversion count and survey tie-point RMS
from `/app/examples`. The winning latitude drives the exported final profile.
When the header disagrees, a QC flag is recorded.

The implementation emits independently graded products for normalized input,
downcast segmentation, depth and derived profiles, binned profiles, latitude
diagnosis, QC flags, the final binned profile, and provenance. Staged and
complete runs must be byte-identical.

The task is clean-room: casts, formulas, tie points, and expected outputs are
generated specifically for this project. Visible campaigns demonstrate every
rule; hidden campaigns rename, resize, and recombine those behaviors, including
a lying header latitude in hidden-beta.

The long horizon comes from seven dependent stages—strict ingestion, downcast
split, latitude-dependent depth conversion, derived properties, depth binning,
latitude QC, and canonical export—rather than from oversized fixtures or
undocumented edge cases.

Success requires three deterministic Oracle rewards of 1.0, NOP and adversarial
rewards of 0.0, a clean Harbor/TB4 package, and an official Stage 2 median
above 80 assistant turns.
