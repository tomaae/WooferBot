#!/bin/sh
rm -rf build dist

echo Python build
python3 -m pipenv run pyinstaller --clean -y wooferbot_cli.spec

echo Copying data
cp README.md dist/
cp LICENSE.md dist/
cp -r src_cli/Overlay.html dist/
mkdir dist/images
cp -r src_cli/images/__place_images.txt dist/images/
cp -r src_cli/mascots dist/
mkdir dist/scripts
cp -r src_cli/scripts/__place_scripts.txt dist/scripts/

