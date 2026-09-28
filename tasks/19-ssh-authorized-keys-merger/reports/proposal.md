# Stage 0 proposal: Rebuild the SSH authorized-keys merger

Proposed slug: `ssh-authorized-keys-merger`

Category: Software

Subcategory: Systems  

Estimated expert time: 5 hours

Identity management exported authorized-keys fragments from several teams in random order. The merger that deduplicates keys, preserves comments, and orders principals lexicographically was lost. The solver rebuilds it to output a canonical keys file and a provenance report listing suppressed duplicates and invalid lines.

Verification parses keys independently, checks OpenSSH formatting, comment preservation, and rejection of malformed entries without altering previous successful merges. Hidden inputs rename principals and include near-duplicate keys with different options.

Standard access-management work; experts can finish quickly because OpenSSH parsing rules are well known, but exact canonical output still requires care.
