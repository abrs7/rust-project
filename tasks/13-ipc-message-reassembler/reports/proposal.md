# Stage 0 proposal: Restore the IPC message reassembler

Proposed slug: `ipc-message-reassembler`

Category: Software

Subcategory: Systems  

Estimated expert time: 8 hours

A microservice mesh dumped fragmented binary messages across sharded capture files after a broker upgrade. The solver rebuilds a library that joins fragments by session, sequence, and checksum, drops duplicates with stable tie-breaking, and exports ordered message streams plus a gap report. Fragment order and shard names are meaningless.

Failed runs exit nonzero without altering a previous successful output set. Verification recomputes joins independently, checks CRC handling, duplicate resolution, and monotonic sequence export. Hidden campaigns introduce torn frames, overlapping sequences, and empty sessions that must fail cleanly. Successful reruns over reshuffled shards must be byte-identical.

The task rewards careful binary parsing and stateful reassembly—common in systems work—but stays bounded because all traps are synthetic and fully documented in the spec bundle.
