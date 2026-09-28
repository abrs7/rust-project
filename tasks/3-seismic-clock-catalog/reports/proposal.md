# Stage 0 proposal: Seismic Clock Catalogue

Proposed slug: `seismic-clock-catalog`

Category: Science

Implementation language: Python standard library

Estimated expert time: 12–16 hours

A synthetic seismic network recorded the same sequence of events at several
stations. Most station clocks remained reliable, but one recorder drifted and
jumped during the campaign. Its faulty timestamps now make valid arrivals look
out of order and can even place a recorded pick before the event that produced
it.

The task is to rebuild the lost processing package and recover the event
catalogue. The supplied campaign contains station definitions, a finite source
grid, exact integer travel times, a small set of surveyed shots, and shuffled
CSV shards of arrival picks. Pick identifiers, filenames, and row order carry
no event or station-clock meaning.

The solution begins by loading and validating the campaign. Exact duplicate
picks are collapsed, conflicting identifiers are rejected, and all definitions
are normalized into a deterministic form.

The reliable stations are then treated as a shared reference clock. For each
possible source location, the supplied travel time is subtracted from each
recorded arrival. Picks produced by the same event should agree on one origin
time. Testing this consistency while excluding each station identifies the
unique faulty recorder and recovers the surveyed and natural events observed
by the stable network.

For every pick from the faulty station, the solver computes a signed residual:

```text
recorded time - event origin - expected travel time
```

The residual is the clock error and may be positive or negative. Several
locally plausible assignments are intentionally present, so greedy
nearest-neighbour matching is insufficient. The solver must build a monotone
assignment lattice and recover the unique chronological path.

The selected path is fitted with the smallest valid piecewise-affine clock
model. Segment rates come from candidate-visible reduced fractions, clock
jumps occur only at declared boundaries, and rational terms use exact
half-away-from-zero rounding. The model is inverted to correct every accepted
arrival. A corrected pick must equal the event origin plus the station's
travel time.

Every input pick receives exactly one accepted or rejected disposition. The
implementation emits independently graded products for normalized input,
network diagnosis, the stable catalogue, residual alternatives, the clock
model, corrected assignments, rejections, the final catalogue, and
provenance. Staged and complete runs must be byte-identical.

The task is clean-room: station geometry, travel times, clock faults, picks,
events, and expected outputs are generated specifically for this project. No
public seismic catalogue or published benchmark is used. Visible campaigns
demonstrate every rule; hidden campaigns only rename, resize, and recombine
those behaviors.

The long horizon comes from seven dependent stages—strict ingestion, faulty
station diagnosis, stable catalogue recovery, global residual assignment,
exact clock fitting, clock inversion and reconciliation, and canonical
export—rather than from oversized fixtures or undocumented edge cases.

Success requires three deterministic Oracle rewards of 1.0, NOP and
adversarial rewards of 0.0, a clean Harbor/TB4 package, and an official Stage
2 median above 80 assistant turns.
