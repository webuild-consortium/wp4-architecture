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
    npx @puppeteer/browsers install chrome@145.0.7632.46
    echo CHROME_DEVEL_SANDBOX=$CHROME_DEVEL_SANDBOX
    sudo chown root:root $CHROME_DEVEL_SANDBOX
    sudo chmod 4755 $CHROME_DEVEL_SANDBOX

    ./install-quarto.sh
}

export CHROME_DEVEL_SANDBOX=$(realpath -m chrome/linux-145.0.7632.46/chrome-linux64/chrome_sandbox)

if [ "$1" == "--github-action" ]; then
    setup
fi

. .venv/bin/activate

./build-quarto.py

# Copy main content
mkdir -p ../build_outputs_folder/blueprint/
cp -R _site/* ../build_outputs_folder/blueprint/
# Copy images
for IMAGE in $(find . -maxdepth 1 -name "*.png") $(find . -maxdepth 1 -name "*.svg") $(find . -maxdepth 1 -name "*.jpg"); do
    echo "Copying image: ${IMAGE}"
    cp ${IMAGE} ../build_outputs_folder/blueprint/
done
if [ -d "../images" ]; then
    rm -rf ../build_outputs_folder/images/
    cp -R ../images ../build_outputs_folder/
fi
