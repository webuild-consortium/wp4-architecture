#!/usr/bin/env python3

import json
import os
import re
import shutil
import subprocess
import sys

SECTION_MD_INPUTS = [
    "01-executive-summary.md",
    "02-regulatory-alignment.md",
    "03-architecture-overview.md",
    "04-integration-model.md",
    "05-data-and-semantics.md",
    "06-trust-and-security.md",
    "07-governance-and-adr.md",
    "08-test-and-validation.md",
    "09-roadmap.md",
]
APPENDIX_MD_INPUTS = [
    "appendix-glossary.md",
    "appendix-history.md",
    "appendix-trust-ecosystem.md",
    "appendix-ebw-definition.md",
    "appendix-wallet-implementation-models.md",
]

def include(blueprint_qmd, qmd: str, indent: int = 1):
    blueprint_qmd.write("::: {.shift-headings by=" + str(indent) + "}\n")
    blueprint_qmd.write("{{< include " + qmd + " >}}\n")
    blueprint_qmd.write(":::\n")
    blueprint_qmd.write("\n")


def generate_qmd(md: str, numbered: bool) -> str:
    with open(md, "r") as md_file:
        lines = [line for line in md_file]
    qmd = md.replace(".md", ".qmd")
    # Add section anchor
    if len(lines) > 0 and lines[0].startswith("#"):
        sec_anchor = "sec-" + qmd.split("--")[0].replace(".", "_").replace("-", "_")
        lines[0] = lines[0][:-1] + " {#" + sec_anchor + "}" + "\n"
    if not numbered:
        for line in lines:
            if line.startswith("#"):
                lines += " {.unnumbered}"
    with open(qmd, "w") as qmd_file:
        for line in lines:
            # Fix Mermaid syntax for Quarto
            line = line.replace('```mermaid', '```{mermaid}')
            qmd_file.write(line)
    return qmd


def get_indexed_mds(index_file: str) -> list[str]:
    mds = []
    index_found = False
    with open(index_file, "r") as f:
        for line in f:
            if "BEGIN INDEX" in line:
                index_found = True
            elif "END INDEX" in line:
                break
            elif index_found and "(" in line and ".md)" in line:
                md = line[line.rfind("(") + 1:line.rfind(".md)") + 3]
                mds.append(md)
    return mds


def generate_adr_appendix():
    print("Generating ADR appendix...")
    generate_qmd("appendix-adr.md", numbered=True)
    base_path = "../adr/"
    adr_mds = get_indexed_mds(base_path + "README.md")
    with open("appendix-adr.qmd", "a") as adr_appendix_qmd:
        for adr_md in adr_mds:
            print("Found ADR:", adr_md)
            shutil.copy(base_path + adr_md, adr_md)
            include(adr_appendix_qmd, generate_qmd(adr_md, numbered=True), indent=2)
    print()


def generate_cs_appendix():
    print("Generating CS appendix...")
    generate_qmd("appendix-cs.md", numbered=True)
    base_path = "../conformance-specs/"
    cs_mds = get_indexed_mds(base_path + "README.md")
    with open("appendix-cs.qmd", "a") as cs_appendix_qmd:
        for cs_md in cs_mds:
            print("Found CS:", cs_md)
            shutil.copy(base_path + cs_md, cs_md)
            include(cs_appendix_qmd, generate_qmd(cs_md, numbered=True), indent=2)
    print()
            

def main():
    generate_adr_appendix()
    generate_cs_appendix()
    
    with open("blueprint.qmd", "w") as blueprint_qmd:
        for md in SECTION_MD_INPUTS:            
            print("Processing:", md)
            qmd = generate_qmd(md, numbered=True)
            print("Generated:", qmd)
            include(blueprint_qmd, qmd)
            
        for md in APPENDIX_MD_INPUTS:
            print("Processing:", md)
            qmd = generate_qmd(md, numbered=True)
            print("Generated:", qmd)
            include(blueprint_qmd, qmd)

        include(blueprint_qmd, "appendix-adr.qmd")
        include(blueprint_qmd, "appendix-cs.qmd")

    if len(sys.argv) > 1 and "html" in sys.argv or "pdf" in sys.argv or "docx" in sys.argv:
        subprocess.run(["quarto", "render", "blueprint.qmd", "--to", sys.argv[1]])
    else:
        subprocess.run(["quarto", "render", "blueprint.qmd", "--to", "html"])
        subprocess.run(["quarto", "render", "blueprint.qmd", "--no-clean", "--to", "pdf"])
        subprocess.run(["quarto", "render", "blueprint.qmd", "--no-clean", "--to", "docx"])
    # Make permissions generic so that builds can work outside Docker
    subprocess.run(["chmod", "-R", "agu+w", "_book", ".quarto"])


if __name__ == "__main__":
    main()
