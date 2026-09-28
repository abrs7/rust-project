# Stage 0 proposal: Fix the bytecode disassembler

Proposed slug: `bytecode-disassembler`

Category: Software

Subcategory: Languages  

Estimated expert time: 9 hours

A teaching VM ships synthetic bytecode files with opcodes documented in a table. The disassembler must decode instructions, resolve jump targets, and write human-readable listings with stable label names derived by contract rules—not by discovery order.

Failed runs exit nonzero without altering a previous successful output set. The verifier compares listing bytes independently, checks jump alignment, unknown opcode rejection, and hidden programs with overlapping jump tables.

VM tooling is classic languages work; experts with interpreter experience can finish within a day using the opcode spec alone.
