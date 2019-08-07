echo "Inserisci il commit: "
read input_variable
echo "Rimuovo le platforms..."
#ionic cordova platforms rm ios
#ionic cordova platforms rm android
#ionic cordova platforms rm browser
git add *
git add -u
git commit -m "$input_variable"
git push
