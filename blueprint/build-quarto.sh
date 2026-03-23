#!/usr/bin/env bash

function setup() {
    sudo apt install -y unzip wget

    # Set up Python environment
    if [ ! -d ".venv" ]; then
	python3 -m venv .venv
	. .venv/bin/activate
	pip install -r ../requirements.txt
    fi

    # Set up Mermaid environment
    npm install -g @mermaid-js/mermaid-cli
}

function extract_last_parenthesis() {
    grep --color=none '.md)$' | rev | cut -d ')' -f 2 | cut -d '(' -f 1 | rev
}

function translate_mermaid_blocks() {
    sed -e "s/\`\`\`mermaid/\`\`\`{mermaid}/"
}

function disable_numbering() {
    sed -i -e 's/\(^##* .*\)/\1 {.unnumbered}/' $1
}

if [ "$1" == "--github-action" ]; then
    setup
fi

. .venv/bin/activate

for CHAPTER in 01-executive-summary.md 02-regulatory-alignment.md 03-architecture-overview.md 04-integration-model.md 05-data-and-semantics.md 06-trust-and-security.md 07-governance-and-adr.md 08-test-and-validation.md 09-roadmap.md appendix-glossary.md appendix-history.md appendix-trust-ecosystem.md appendix-ebw-definition.md appendix-wallet-implementation-models.md appendix-adr.md; do
    echo "Processing: ${CHAPTER}"
    cat ${CHAPTER} | translate_mermaid_blocks > $(basename ${CHAPTER} .md).qmd
done

# ADR appendix, gathers all ADRs
for ADR in $(cat ../adr/README.md | extract_last_parenthesis); do
    echo "Adding ADR: ${ADR}"
    QMD_ADR=../adr/$(basename ${ADR} .md).qmd
    cat ../adr/${ADR} | translate_mermaid_blocks > ${QMD_ADR}
    echo >> appendix-adr.qmd
    echo '::: {.shift-headings by=2}' >> appendix-adr.qmd
    echo "{{< include ${QMD_ADR} >}}" >> appendix-adr.qmd
    echo ':::' >> appendix-adr.qmd
done

for APPENDIX in appendix-glossary.qmd appendix-history.qmd appendix-trust-ecosystem.qmd appendix-ebw-definition.qmd appendix-wallet-implementation-models.qmd appendix-adr.qmd ../adr/*.qmd; do
    disable_numbering ${APPENDIX}
done

echo "Building HTML..."
/usr/bin/time quarto render blueprint.qmd --to html

# echo "Building PDF..."
# /usr/bin/time quarto render blueprint.qmd --no-clean --to pdf

# echo "Building DOCX..."
# /usr/bin/time quarto render blueprint.qmd --no-clean --to docx
