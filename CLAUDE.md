# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository purpose

This is a **documentation and governance** repository for the WE BUILD consortium's WP4 Architecture Group — it contains no application code. Contributions are Markdown documents that flow through a defined governance process and are compiled into a published deliverable (D4.1).

Three artifact types, each with its own lifecycle and template:

- **ADRs** ([adr/](adr/)) — lightweight Architecture Decision Records, one per software decision affecting interoperability. Template: [adr/_template.md](adr/_template.md). New ADRs must be added to the numbered list in [adr/README.md](adr/README.md) between the `<!--BEGIN INDEX-->` / `<!--END INDEX-->` markers — that list is the source of truth the blueprint build reads from.
- **Conformance Specifications (WBCS / CSs)** ([conformance-specs/](conformance-specs/)) — normative implementation requirements translating ADR decisions into testable specs (RFC 2119 language). Template: [conformance-specs/_template.md](conformance-specs/_template.md). Approved CSs go in the "Approved WBCSs" table in [conformance-specs/README.md](conformance-specs/README.md); the build reads CS filenames from any `.md)` link in that README.
- **Blueprint (D4.1)** ([blueprint/](blueprint/)) — the consolidated deliverable. Authored as numbered chapter files (`01-executive-summary.md` … `09-roadmap.md`) plus `appendix-*.md` files; the build assembles these together with the ADR and CS appendices into a single HTML and PDF.

Drafts that aren't yet mature live in [webuild-drafts/](webuild-drafts/).

## Building the Blueprint

The build is a multi-stage shell pipeline in [blueprint/build.sh](blueprint/build.sh) that assembles every chapter + every ADR + every CS into one Markdown file, converts to AsciiDoc via `kramdoc`, and renders HTML and PDF via `asciidoctor` / `asciidoctor-pdf`. It is run from inside `blueprint/`:

```sh
cd blueprint
./build.sh                  # incremental local build (assumes deps already installed)
./build.sh --github-action  # also runs setup() to install Ruby, Python, Mermaid CLI, Chrome
```

Outputs land in `build_outputs_folder/blueprint/` (`blueprint.html`, `blueprint.pdf`, plus copied images). The `.venv/` Python environment is created on first `--github-action` run and reactivated on subsequent runs.

CI ([.github/workflows/build-blueprint.yml](.github/workflows/build-blueprint.yml)) runs the build on push to `main`, `asciidoc`, or `blueprint-preview` and deploys to GitHub Pages. Published at:
- https://webuild-consortium.github.io/wp4-architecture/blueprint/blueprint.html
- https://webuild-consortium.github.io/wp4-architecture/blueprint/blueprint.pdf

Dependencies (only needed when building locally):
- Ruby gems: `kramdown-asciidoc`, `asciidoctor-diagram`, `asciidoctor-pdf` (see [blueprint/Gemfile](blueprint/Gemfile))
- Python (in `blueprint/.venv`): `enumerate-markdown`, `mistune==2.0.5` (see [requirements.txt](requirements.txt)) — provides the `markdown-enum` command used to number sections
- Node: `@mermaid-js/mermaid-cli` plus a pinned Chrome (`chrome@145.0.7632.46`) for diagram rendering

## Things that will trip you up in the build

- **The QTSP appendix is fetched from a sibling repo at build time** — `collect_qtsp_appendix` in [blueprint/build.sh](blueprint/build.sh) downloads `webuild-consortium/wp4-qtsp-group` as a zip and stitches READMEs together into `appendix-qtsp.md`. Don't commit `appendix-qtsp.md`, `qtsp-main.zip`, or the unpacked `wp4-qtsp-group-main/` directory.
- **ADR and CS appendices are auto-included from the `README.md` files in those directories.** To add an ADR or CS to the blueprint, edit the relevant README — don't touch `build.sh`. The build extracts `.md)` link targets from `adr/README.md` and `conformance-specs/README.md`.
- **Header levels get shifted** during inclusion (`indent_headers` is applied twice to each ADR/CS so a top-level `#` in the source becomes `###` in the blueprint). Author ADR/CS files as standalone documents with normal `#` headings; do not pre-shift.
- **The CS `_template.md` is escaped specially** — `<` and `>` are replaced with `&lt;` / `&gt;` before inclusion so AsciiDoc doesn't interpret placeholder angle brackets as tags. This is handled in `build.sh`; the template itself uses literal `<` / `>`.
- **Table column widths are patched post-conversion** via `table_width` in `build.sh`, keyed on the header text of specific tables in `main.adoc`. If you change those header rows in the source Markdown, also update the matching `fgrep` strings in `build.sh`.

## Governance

- All files are reviewed by `@webuild-consortium/blueprint-coordination-group` ([.github/CODEOWNERS](.github/CODEOWNERS)).
- Workflow: open an issue → discuss → PR → BCG review and merge. The ADR process diagram lives in [adr/README.md](adr/README.md).
- Once an ADR is merged it is the consortium's decision; dissenting views are captured in the **Advice** section of the ADR rather than blocking the merge.
