#!/usr/bin/env python3

import json
import os
import re
import shutil
import subprocess
import sys
from collections import defaultdict

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
    "appendix-glossary.md",
    "appendix-history.md",
]
HEADINGS = [
    "blueprint.qmd",
    "appendix-adr.qmd",
    "appendix-cs.qmd",
    "appendix-ebw-definition.qmd",
    "appendix-trust-ecosystem.qmd",
    "appendix-qtsp.qmd",
]

def include(blueprint_qmd, qmd: str, indent: int = 1):
    blueprint_qmd.write("::: {.shift-headings by=" + str(indent) + "}\n")
    blueprint_qmd.write("{{< include " + qmd + " >}}\n")
    blueprint_qmd.write(":::\n\n")


def generate_qmd(md: str, numbered: bool) -> str:
    with open(md, "r") as md_file:
        lines = [line for line in md_file]
    qmd = md.replace(".md", ".qmd")
    for i, line in enumerate(lines):
        tags = set()
        if line.startswith("#"):
            if i == 0:
                # Add section anchor
                tags.add("#sec-" + qmd.split("--")[0].replace(".", "_").replace("-", "_").replace("/", "_"))
            if not numbered:
                tags.add(".unnumbered")
            if tags:
                lines[i] = lines[i][:-1] + " {" + " ".join(tags) + "}\n"
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
            include(adr_appendix_qmd, generate_qmd(adr_md, numbered=True), indent=1)
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
            include(cs_appendix_qmd, generate_qmd(cs_md, numbered=True), indent=1)
    print()


def fix_qtsp_doc(filename: str):
    with open(filename, "r") as file:
        lines = [line for line in file]
    with open(filename, "w") as file:
        for line in lines:
            # Fix links
            line = line.replace('.../README.md', 'https://github.com/webuild-consortium/wp4-qtsp-group/blob/main/README.md')
            for md in ["architecture.md", "issuance-to-eudiw.feature.md", "validation.feature.md", "verification.feature.md", "rb0xx_hello_world_attestation.md"]:
                line = line.replace(md, f"https://github.com/webuild-consortium/wp4-qtsp-group/blob/main/docs/qeaa/{md}")
            file.write(line)
    
def generate_qtsp_appendix():
    from pathlib import Path
    if not Path("qtsp-main.zip").exists():
        subprocess.run(["wget", "https://github.com/webuild-consortium/wp4-qtsp-group/archive/refs/heads/main.zip", "-O", "qtsp-main.zip"])
        subprocess.run(["unzip", "qtsp-main.zip"])
    print("Generating QTSP appendix...")
    generate_qmd("appendix-qtsp.md", numbered=True)
    with open("appendix-qtsp.qmd", "a") as appendix_qtsp:
        for readme in ["qes/README.md", "qeaa/README.md", "qerds/README.md", "rwscd/README.md", "rpac-rprc/README.md"]:
            readme_path = f"wp4-qtsp-group-main/docs/{readme}"
            print(f"Processing: {readme_path}")
            readme_qmd = generate_qmd(readme_path, numbered=True)
            fix_qtsp_doc(readme_qmd)
            include(appendix_qtsp, readme_qmd, indent=1)
    print()

    # for IMAGE in $(find . -name "*.svg"); do
    #     echo "Copying: ${IMAGE}"
    #     cp ${IMAGE} ${BUILD_DIR}
    # done


def generate_blueprint():
    with open("blueprint.qmd", "w") as blueprint_qmd:
        for md in SECTION_MD_INPUTS:            
            print("Processing:", md)
            qmd = generate_qmd(md, numbered=(not md.startswith("appendix")))
            print("Generated:", qmd)
            include(blueprint_qmd, qmd)


def main():
    generate_blueprint()
    generate_adr_appendix()
    generate_cs_appendix()
    generate_qmd("appendix-ebw-definition.md", numbered=True)
    generate_qmd("appendix-trust-ecosystem.md", numbered=True)
    generate_qtsp_appendix()

    if len(sys.argv) > 1 and "html" in sys.argv or "pdf" in sys.argv or "docx" in sys.argv:
        subprocess.run(["quarto", "render", *HEADINGS, "--to", sys.argv[1]])
    else:
        subprocess.run(["quarto", "render", *HEADINGS, "--to", "html"])
        # subprocess.run(["quarto", "render", *HEADINGS, "--no-clean", "--to", "pdf"])
        subprocess.run(["quarto", "render", *HEADINGS, "--no-clean", "--to", "docx"])
    # Make permissions generic so that builds can work outside Docker
    subprocess.run(["chmod", "-R", "agu+w", "_site", ".quarto"])


if __name__ == "__main__":
    main()
