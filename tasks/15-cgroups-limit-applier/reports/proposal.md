# Stage 0 proposal: Recover the cgroups limit applier

Proposed slug: `cgroups-limit-applier`

Category: Software

Subcategory: Systems  

Estimated expert time: 9 hours

A container host lost the tool that translates YAML limit profiles into cgroup v2 settings for synthetic workloads. Campaigns supply profile shards, process maps, and worked examples with expected resulting limit files. The rebuilt applier must normalize inputs, resolve conflicts, and write canonical limit artifacts without touching unrelated profiles.

Failed runs exit nonzero without altering a previous successful output set. Verification independently derives limit files from the contract formulas, checks conflict failures, and ensures staged regeneration is deterministic across shuffled inputs. Hidden campaigns vary CPU, memory, and IO combinations plus conflicting inheritance rules.

This is realistic capacity-management work compressed into a clean-room exercise; expert time stays moderate because the cgroup mapping is fully specified in bundled JSON schemas.
