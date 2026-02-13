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

export GEM_HOME="$HOME/gems"
export PATH="$HOME/gems/bin:$PATH"
export CHROME_DEVEL_SANDBOX=$(realpath -m chrome/linux-145.0.7632.46/chrome-linux64/chrome_sandbox)

if [ "$1" == "--github-action" ]; then
    setup
fi

. .venv/bin/activate

echo '# WE BUILD – Architecture & Integration Blueprint (D4.1)' > main.md
cat 01-executive-summary.md >> main.md

rm -f main-body.md
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

cat main-body-enum.md >> main.md

echo >> main.md
cat appendix-trust-ecosystem.md >> main.md

echo >> main.md
cat appendix-glossary.md >> main.md

echo >> main.md
cat appendix-history.md >> main.md

echo "Running kramdoc..."
kramdoc --auto-ids main.md -o main.adoc

ASCIIDOC_ARGS="-r asciidoctor-diagram -a allow-uri-read -a toc=left --doctype book"

echo "Generating HTML..."
asciidoctor ${ASCIIDOC_ARGS} main.adoc

echo "Generating PDF..."
asciidoctor-pdf ${ASCIIDOC_ARGS} main.adoc --out-file blueprint.pdf

mkdir -p ../build_outputs_folder/blueprint
cp main.html ../build_outputs_folder/blueprint/index.html
cp *png ../build_outputs_folder/blueprint/
cp blueprint.pdf ../build_outputs_folder/blueprint/blueprint.pdf
