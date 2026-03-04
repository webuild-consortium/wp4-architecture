#!/usr/bin/env bash


function setup() {
    # Set up Ruby environment to make kramdoc/asciidoc available:
    sudo apt install -y ruby-dev ruby-bundler
    bundle install

    # Set up Python environment
    if [ ! -d ".venv" ]; then
	python3 -m venv .venv
	. .venv/bin/activate
	pip install -r ../requirements.txt
    fi

    # Set up Mermaid environment
    npm install -g @mermaid-js/mermaid-cli
    npx @puppeteer/browsers install chrome@145.0.7632.46
    echo CHROME_DEVEL_SANDBOX=$CHROME_DEVEL_SANDBOX
    sudo chown root:root $CHROME_DEVEL_SANDBOX
    sudo chmod 4755 $CHROME_DEVEL_SANDBOX
}

function indent_headers() {
    sed -e 's/^#### /##### /g' | sed -e 's/^### /#### /g' | sed -e 's/^## /### /g' | sed -e 's/^# /## /g'
}

function extract_last_parenthesis() {
    grep --color=none '.md)$' | rev | cut -d ')' -f 2 | cut -d '(' -f 1 | rev
}

function extract_last_parenthesis_in_line() {
    grep --color=none '.md)' | rev | cut -d ')' -f 2 | cut -d '(' -f 1 | rev
}

export GEM_HOME="$HOME/gems"
export PATH="$HOME/gems/bin:$PATH"
export CHROME_DEVEL_SANDBOX=$(realpath -m chrome/linux-145.0.7632.46/chrome-linux64/chrome_sandbox)

if [ "$1" == "--github-action" ]; then
    setup
fi

. .venv/bin/activate

rm -f main-body.md
cat 01-executive-summary.md >> main-body.md
echo >> main-body.md
cat 02-regulatory-alignment.md >> main-body.md
echo >> main-body.md
cat 03-architecture-overview.md >> main-body.md
echo >> main-body.md
cat 04-integration-model.md >> main-body.md
echo >> main-body.md
cat 05-data-and-semantics.md >> main-body.md
echo >> main-body.md
cat 06-trust-and-security.md >> main-body.md
echo >> main-body.md
cat 07-governance-and-adr.md >> main-body.md
echo >> main-body.md
cat 08-test-and-validation.md >> main-body.md
echo >> main-body.md
cat 09-roadmap.md >> main-body.md
echo >> main-body.md

rm -f main-body-enum.md
markdown-enum main-body.md 1 main-body-enum.md

rm -f main.md

cat main-body-enum.md >> main.md

echo >> main.md
cat appendix-glossary.md >> main.md

echo >> main.md
cat appendix-history.md >> main.md

echo >> main.md
cat appendix-trust-ecosystem.md >> main.md

echo >> main.md
cat appendix-ebw-definition.md >> main.md

# ADR appendix, gathers all ADRs
echo >> main.md
cat appendix-adr.md >> main.md
for ADR in $(cat ../adr/README.md | extract_last_parenthesis); do
    echo "Adding ADR: ${ADR}"
    echo >> main.md
    cat ../adr/${ADR} | indent_headers | indent_headers >> main.md
done

# CS appendix, gathers all conformance specifications
echo >> main.md
cat appendix-cs.md >> main.md
for CS in $(cat ../conformance-specs/README.md | extract_last_parenthesis_in_line); do
    echo "Adding CS: ${CS}"
    echo >> main.md
    cat ../conformance-specs/${CS} | indent_headers | indent_headers >> main.md
done

echo "Running kramdoc..."
kramdoc --auto-ids --heading-offset 1 main.md -o main.adoc

# Prepend title to fix header level and TOC placement
TMP_FILE=$(mktemp)
echo '= WE BUILD -- Architecture & Integration Blueprint (D4.1)' >> ${TMP_FILE}
echo >> ${TMP_FILE}
cat main.adoc >> ${TMP_FILE}
mv ${TMP_FILE} main.adoc

ASCIIDOC_ARGS="-r asciidoctor-diagram -a allow-uri-read --doctype article --verbose -a toclevels=3"

# Set SVG output mode for Mermaid diagrams
sed -e 's/\[mermaid\]/[mermaid, format=svg]/g' main.adoc > main-svg.adoc

echo "Generating HTML..."
asciidoctor ${ASCIIDOC_ARGS} -a toc=left -a stylesheet=asciidoctor.css main-svg.adoc -o blueprint.html

echo "Generating PDF..."
asciidoctor-pdf ${ASCIIDOC_ARGS} -a toc=auto main.adoc -a pdf-theme=pdf -a pdf-themesdir=. -a title-page=true --out-file blueprint.pdf

mkdir -p ../build_outputs_folder/blueprint
cp blueprint.html ../build_outputs_folder/blueprint/blueprint.html
cp blueprint.pdf ../build_outputs_folder/blueprint/blueprint.pdf
for IMAGE in $(find . -maxdepth 1 -name "*.png") $(find . -maxdepth 1 -name "*.svg") $(find . -maxdepth 1 -name "*.jpg"); do
    cp ${IMAGE} ../build_outputs_folder/blueprint/
done
