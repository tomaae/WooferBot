@ECHO OFF
SET VERSION=1.6

if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

REM Python build
pipenv run pyinstaller --clean -y wooferbot_cli.spec

mkdir dist\WooferBot-%VERSION%-Win

REM Copying data
cp dist\wooferbot_cli.exe dist\WooferBot-%VERSION%-Win\
cp README.md dist\WooferBot-%VERSION%-Win\
cp LICENSE.md dist\WooferBot-%VERSION%-Win\
cp -r src\Overlay.html dist\WooferBot-%VERSION%-Win\
mkdir dist\WooferBot-%VERSION%-Win\images
cp -r src\images\__place_images.txt dist\WooferBot-%VERSION%-Win\images\
cp -r src\mascots dist\WooferBot-%VERSION%-Win\
mkdir dist\WooferBot-%VERSION%-Win\scripts
cp -r src\scripts\__place_scripts.txt dist\WooferBot-%VERSION%-Win\scripts\
rmdir /s /q dist\WooferBot-%VERSION%-Win\mascots\tomaae

cd dist
zip -r WooferBot-%VERSION%-Win.zip WooferBot-%VERSION%-Win
cd ..

REM Prepare linux
mkdir dist\WooferBot-%VERSION%-Linux\
cp -r dist\WooferBot-%VERSION%-Win\* dist\WooferBot-%VERSION%-Linux\
rm dist\WooferBot-%VERSION%-Linux\*.exe
cp src\wooferbot.py dist\WooferBot-%VERSION%-Linux\
cp -r src\lib dist\WooferBot-%VERSION%-Linux\
cp Pipfile dist\WooferBot-%VERSION%-Linux\

cd dist
tar -czvf WooferBot-%VERSION%-Linux.tar.gz WooferBot-%VERSION%-Linux
cd ..