#!/usr/bin/env sh

# pip の更新
pip3 install --user -U pip

# Pyhees レポジトリは Package リリースがされていないため requirements.txt に含めることができない
pip3 install --user git+https://github.com/BRI-EES-House/pyhees.git

