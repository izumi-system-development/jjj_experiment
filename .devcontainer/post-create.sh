#!/usr/bin/env sh

# pip の更新
pip3 install --user -U pip

# numpy, pandas などは Pyhees 使用バージョンが自動的に追加されるため不要
pip3 install --user -r requirements.txt

# Pyhees レポジトリは Package リリースがされていないため requirements.txt に含めることができない

# pip3 install --user git+https://github.com/BRI-EES-House/pyhees.git
pip3 install --user git+https://github.com/izumi-system-development/pyhees.git@smart_installs
