# Stage 0 proposal: Repair the systemd unit generator

Proposed slug: `systemd-unit-generator`

Category: Software

Subcategory: Systems

Estimated expert time: 10 hours

---

## Submission text

A deployment repo lost the generator that merges systemd units from scattered fragments, and the solver rebuilds the Python (stdlib-only) package that materializes installable unit files from a synthetic campaign tree. The tree lists unit basenames (for example app.service), optional main fragments, and drop-in fragments under {basename}.d/*.conf in lexicographic filename order. Each fragment is INI-like: sections [Unit], [Service], [Install], or [Socket] only; keys must appear on an allowed list given in the campaign metadata; values are unparsed strings except Environment= lines, which parse as KEY=VALUE pairs merged by key with later fragments overriding earlier ones for the same KEY. Unknown sections or keys are invalid. Two main fragments defining the same basename in different directories are invalid.

Merging is a fixed policy, not discovery. For each basename, start from the main fragment if present, else empty sections. Apply each drop-in in sorted order: for each section/key, replace the value entirely (Environment= merges keys as above). Emit merged units as UTF-8 text: sections in order Unit, Service, Install, Socket; within each section, keys sorted lexicographically; one Key=value per line with a single space after the equals sign; file ends with one trailing newline. Output directory receives {basename} files. diff.json lists basenames whose merged SHA-256 changed from the campaign's previous_generation hashes (sorted by basename), or marks initial when no previous hash exists. manifest.json lists SHA-256 of every input fragment and output file using canonical JSON (UTF-8, sorted keys, separators , and : without spaces, one trailing newline).

Any invalid campaign exits 2, writes a canonical JSON diagnostic to the separate report path, and leaves any previous output directory byte-identical. Invalid means duplicate basename mains, forbidden section/key, malformed Environment= without equals, or a .d directory whose basename has no corresponding unit type suffix. Duplicate drop-in filenames in one directory are invalid. Verification recomputes merges with an independent reference merger, compares exact unit bytes and JSON on visible and hidden trees with renamed drop-ins, conflicting Environment keys across three layers, and missing mains with drop-ins only. It requires identical output after fragment reordering within directories and checks atomic replacement after success. The ten-hour estimate reflects layered override semantics, Environment merging, and canonical text formatting interacting; one wrong merge order changes unit bytes and downstream diff.json.
