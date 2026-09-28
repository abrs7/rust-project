# Stage 0 proposal: Reconcile the deadlock wait graph

Proposed slug: `deadlock-wait-graph-reconcile`

Category: Software

Subcategory: Databases  

Estimated expert time: 7 hours

Transaction waits were captured as edge lists between synthetic transactions with lock modes. The tool must build a wait-for graph, detect cycles, propose victim transactions by contract tie rules, and export a resolution trace.

Failed runs exit nonzero without altering a previous successful output set. Verification rebuilds graphs and victim choices independently and tests hidden waits with multiple equal-cost victims requiring lexicographic choice.

Deadlock detection is taught in database courses; applying explicit victim tie rules makes it gradable.
