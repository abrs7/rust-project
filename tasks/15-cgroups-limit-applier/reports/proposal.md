# Stage 0 proposal: Recover the cgroups limit applier

Proposed slug: `cgroups-limit-applier`

Category: Software

Subcategory: Systems

Estimated expert time: 12 hours

---

## Submission text

A container host lost the tool that turns YAML limit profiles into cgroup v2 files for synthetic workloads, and the solver rebuilds the Python (stdlib-only) package that materializes controller settings from a campaign. Profiles have IDs, optional parent ID, controllers cpu.max (quota and period as integers separated by space), memory.max (integer bytes or the literal max), and io.max lines device MAJ:MIN rbps wbps riops wiops as space-separated integers or max. Maintenance windows attach to profiles as half-open UTC minute ranges [start, end) during which listed controllers use override limits instead of base limits; overlapping windows for the same profile are invalid. A process map assigns each process ID to a leaf profile ID; processes inherit merged limits by walking parent chain from leaf to root, child overrides parent per controller when both set a value, and missing parent IDs are invalid.

Application is a fixed policy, not tuning. For each distinct leaf profile referenced, emit a directory named by profile ID containing one file per active controller after merge: cpu.max, memory.max, io.max with merged content. Processes group under their leaf profile; emit cgroup.procs listing PIDs sorted ascending as decimal strings one per line, file ending with newline. For each maintenance window on a profile, emit windows/{start_minute}_{end_minute}/ with the same controller files using override values for controllers listed in that window only; other controllers omit from override directory. limits.json summarizes each profile's effective base merge and each window's overrides (controllers touched, sorted keys). manifest.json SHA-256 covers inputs and outputs with canonical JSON rules: UTF-8, sorted keys, separators , and : without spaces, integers only, one trailing newline.

Any invalid campaign exits 2, writes a canonical JSON diagnostic to the separate report path, and leaves any previous output directory byte-identical. Invalid means unknown parent, cyclic inheritance, overlapping maintenance on one profile, unknown process profile, io.max device not matching MAJ:MIN pattern, or quota exceeding period on cpu.max. Verification recomputes merges and window overrides with an independent reference, compares exact bytes on visible and hidden campaigns with three-level inheritance, partial controller overrides, overlapping process groups, and windows spanning midnight UTC. It requires identical output after profile shard reshuffle and checks atomic replacement after success. The twelve-hour estimate reflects inheritance merge, time-bounded overrides, and multi-file cgroup layout interacting; one wrong merge at a parent changes every child process directory.
