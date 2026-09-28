Telemetry Frame Recovery

This task asks the solver to restore a damaged scientific telemetry decoder and use it to reconstruct calibrated observations from a set of synthetic space-spectrometer captures. The working directory contains raw binary sessions from two firmware generations, incomplete engineering notes, startup diagnostics, and a Python package whose framing, timing, and calibration stages are missing. The required deliverables are the repaired command-line decoder, normalized event streams, recovered per-session calibration parameters, and a deterministic manifest that links each source capture to its calibrated output.

The task is designed around empirical reconstruction rather than implementing a protocol copied from a written specification. The supplied evidence is sufficient to recover the behavior, but it is distributed across real bytes, diagnostic counters, calibration sequences, and relationships between sessions. A fixed-record parser produces plausible output on ordinary packets while silently mishandling fragmented frames. A single byte order works for one firmware generation but not the other. Device time crosses a counter rollover in some sessions, and calibration must be inferred from reference events before science samples can be normalized. These properties compound across the deliverables, so an early mistake remains well-formed but changes exact downstream values.

The fixtures and packet format will be generated specifically for this task and will not use a public protocol, dataset, challenge, paper repository, or benchmark implementation. Agent-visible files will not contain expected outputs, hashes of the answers, sequential names that encode values, or a complete parser. Small visible captures will expose evidence for every behavior. Hidden verifier captures will vary fragmentation boundaries, firmware generation, rollover position, calibration coefficients, noise placement, and event ordering.

Verification will be deterministic and independent of the reference solution. The verifier will run in a separate container, compare exact frozen values derived from a separately reviewed protocol definition, and reject missing or partial outputs. It will check framing recovery, event ordering, timestamp reconstruction, calibration parameters, calibrated samples, source-to-output manifests, and behavior on varied hidden sessions. Candidate code will run without access to verifier files or reward paths. Empty output, a constant-output implementation, a parser that assumes one firmware, and a parser that copies visible constants must all score zero.

The task is long-horizon because the solver must inspect heterogeneous evidence, infer the lost framing and timing behavior, restore several dependent components, explore failures across multiple captures, and then produce three mutually consistent artifact families. The main challenge is not data volume or expensive computation; it is reconstructing a scientific data path whose locally plausible shortcuts diverge on exact downstream results.

Proposed slug: telemetry-frame-recovery

Proposed category: scientific-computing

Implementation language: Python

Estimated expert time: 6 hours
