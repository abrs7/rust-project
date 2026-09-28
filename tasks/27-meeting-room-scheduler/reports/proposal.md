# Stage 0 proposal: Fix the meeting room scheduler

Proposed slug: `meeting-room-scheduler`

Category: Software

Subcategory: Algorithms  

Estimated expert time: 5 hours

Facilities management exported room booking requests as shuffled intervals with priorities and room capabilities. The scheduler assigns rooms to maximize covered high-priority minutes under non-overlap constraints with deterministic tie-breaking when choices tie.

Failed runs exit nonzero without altering a previous successful output set. Verification recomputes assignments independently, checks capability filtering, unassigned request reporting, and hidden request sets with equal-priority conflicts.

Classic interval scheduling with extra constraints; solvable in an afternoon with clear scoring rules.
