#!/usr/bin/bash

echo "Changing directory..."
cd ~
echo "Downloading..."
wget https://docs.google.com/uc?id=0B3X9GlR6EmbnWksyTEtCM0VfaFE&export=download
wait
echo "Renaming..."
mv uc\?id\=0B3X9GlR6EmbnWksyTEtCM0VfaFE gdrive
echo "Chaning permissions..."
chmod +x gdrive
echo "Creating install folder..."
mkdir .local
mkdir .local/bin
mkdir .local/bin
echo "Installing..."
install gdrive ~/.local/bin
echo "Go to this link, then paste Google Authentication code..."
~/gdrive list
read
echo "Testing..."
touch test.txt
echo "Google Drive is working!" >> test.txt
~/gdrive upload test.txt
echo "You should now find test.txt under you home google drive directory..."

