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

    ./install-quarto.sh
}

. .venv/bin/activate

./build-quarto.py
