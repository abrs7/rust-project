# Stage 0 proposal: Gamma Spectrum Calibration

Proposed slug: `gamma-spectrum-calibration`

Category: Science

Implementation language: Python standard library

Estimated expert time: 12–16 hours

A synthetic gamma-spectroscopy campaign recorded pulse-height histograms for a
calibration run and a separate measurement spectrum, together with per-pulse
acquisition timestamps. One calibration source line saturated the detector,
producing a wide plateau peak that must be excluded before fitting. The
measurement spectrum was acquired under non-negligible dead time, so reported
counts understate true activity unless corrected from the timestamp log.

The task is to rebuild the lost processing package and recover calibrated line
integrations. The supplied campaign contains calibration line definitions,
shuffled CSV histogram shards, and shuffled timestamp event logs. Shard names,
row order, and identifiers carry no physical meaning.

The solution begins by loading and validating the campaign. Histogram shards
are merged by channel, timestamps are sorted, and all definitions are
normalized into a deterministic form.

Local maxima in the calibration histogram become peak candidates. Each
candidate receives width and plateau evidence. Saturated peaks are excluded
from the linear energy calibration fit. Remaining lines are matched to peaks
in ascending energy order and fit with exact rational coefficients under
round-half-away-from-zero rounding.

Dead-time correction is derived from the timestamp span, event count, and the
per-count dead time constant in the campaign. The correction is applied to
measurement spectrum counts, channels are converted to energy, and each known
line is integrated over a fixed half-width window.

The implementation emits independently graded products for normalized input,
peak candidates, line exclusions, the calibration fit, dead-time correction,
the corrected spectrum, line integrations, the final report, and provenance.
Staged and complete runs must be byte-identical.

The task is clean-room: detector response, calibration lines, histograms,
timestamps, and expected outputs are generated specifically for this project.
No public spectrum library or published benchmark is used. Visible campaigns
demonstrate every rule through sparse examples; hidden campaigns only rename,
resize, and recombine those behaviors with different seeds, saturated line
indices, and dead-time constants.

The long horizon comes from seven dependent stages—strict ingestion, peak
detection, saturation-aware calibration fitting, dead-time derivation,
spectrum correction, line integration, and canonical export—rather than from
oversized fixtures or step-by-step protocol manuals.

Success requires three deterministic Oracle rewards of 1.0, NOP and
adversarial rewards of 0.0, a clean Harbor/TB4 package, and an official Stage
2 median above 80 assistant turns.
