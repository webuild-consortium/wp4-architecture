#!/usr/bin/env bash


function setup() {
    # Set up Ruby environment to make kramdoc/asciidoc available:
    sudo apt install -y ruby-dev ruby-bundler unzip wget
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

function table_width() {
    # args: $1=headers, $2=weights
    let "LINE = $(fgrep -n "$1" main.adoc | cut -d ":" -f 1) - 1"
    TMP_FILE=$(mktemp)
    awk 'NR=='${LINE}'{print "[cols=\"'$2'\"]"}1' main.adoc > ${TMP_FILE}
    mv ${TMP_FILE} main.adoc
}

function collect_qtsp_appendix() {
    if [ ! -f qtsp-main.zip ]; then
	wget https://github.com/webuild-consortium/wp4-qtsp-group/archive/refs/heads/main.zip -O qtsp-main.zip
	unzip qtsp-main.zip
    fi
    rm -f appendix-qtsp.md && touch appendix-qtsp.md
    BUILD_DIR=${PWD}
    QTSP_MD=$(realpath appendix-qtsp.md)
    pushd wp4-qtsp-group-main/docs
    echo '# Appendix F. QTSP documentation' >> ${QTSP_MD}
    echo >> ${QTSP_MD}
    echo 'The WP4 QTSP group collaborates on [internal reference code and documentation](https://github.com/webuild-consortium/wp4-qtsp-group) to increase interoperability. This appendix lists the entry points for this reference documentation by each provided service.' >> ${QTSP_MD}
    for README in qes/README.md qeaa/README.md qerds/README.md rwscd/README.md rpac-rprc/README.md; do
	echo >> ${QTSP_MD}
	cat ${README} | indent_headers >> ${QTSP_MD}
	echo >> ${QTSP_MD}
    done
    sed -i -e 's/..\/README.md/https:\/\/github.com\/webuild-consortium\/wp4-qtsp-group\/blob\/main\/README.md/g' ${QTSP_MD}
    for MD in architecture.md issuance-to-eudiw.feature.md validation.feature.md verification.feature.md rb0xx_hello_world_attestation.md; do
	sed -i -e "s/${MD}/https:\/\/github.com\/webuild-consortium\/wp4-qtsp-group\/blob\/main\/docs\/qeaa\/${MD}/g" ${QTSP_MD}
    done
    for IMAGE in $(find . -name "*.svg"); do
	echo "Copying: ${IMAGE}"
	cp ${IMAGE} ${BUILD_DIR}
    done
    popd
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

echo >> main.md
cat appendix-wallet-implementation-models.md >> main.md

collect_qtsp_appendix
echo >> main.md
cat appendix-qtsp.md >> main.md

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
    if [ "$CS" == "_template.md" ]; then
	cp ../conformance-specs/$CS _template_escaped.md
	sed -i -e 's/</\&lt;/g' _template_escaped.md
	sed -i -e 's/>/\&gt;/g' _template_escaped.md
	CS_PATH=_template_escaped.md
    else
	CS_PATH=../conformance-specs/${CS}
    fi
    echo "Adding CS: ${CS}"
    echo >> main.md
    cat $CS_PATH | indent_headers | indent_headers >> main.md
done

echo "Running kramdoc..."
kramdoc --auto-ids --heading-offset 1 main.md -o main.adoc

echo "Fixing tables..."
table_width 'Version | Date | Author | Description' '2,2,3,2'
table_width '| *Month* | *Type* | *Reference and Title* | *Connection to D4.1*' '1,1,3,3'

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
if [ -d "../images" ]; then
    rm -rf ../build_outputs_folder/images/
    cp -R ../images ../build_outputs_folder/
fi
