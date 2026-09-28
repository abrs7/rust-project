# Stage 0 proposal: Rebuild the INI configuration parser

Proposed slug: `ini-configuration-parser`

Category: Software

Subcategory: Languages  

Estimated expert time: 6 hours

Services still load INI files with nested sections, continuation lines, and quoted values. The parser must emit a canonical JSON representation with stable key ordering and precise error locations for invalid input.

Failed runs exit nonzero without altering a previous successful output set. The verifier compares JSON bytes for visible and hidden INI files, including duplicate keys, invalid escapes, and mixed line endings.

Config parsers are language-tooling bread and butter; experts can implement one in hours given explicit grammar notes.
