# Stage 0 proposal: Repair the systemd unit generator

Proposed slug: `systemd-unit-generator`

Category: Software

Subcategory: Systems  

Estimated expert time: 7 hours

A deployment repo contains service descriptions, environment overlays, and socket units scattered across nested directories, but the generator that merges them into installable unit files was deleted. The solver must rebuild it so that merged units honor override precedence, drop unknown keys, and emit a deterministic bundle plus a diff manifest against the previous generation.

The verifier checks merged unit bytes, precedence rules, invalid key rejection, and preservation of prior output on failure. Hidden trees rename units, add drop-in conflicts, and swap dependency directions. No internet or host-specific paths are involved.

Anyone who has packaged services for Linux can solve this within a day; the challenge is encoding override semantics precisely enough for independent verification.
