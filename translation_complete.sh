#!/bin/bash
mkdir lala; 
./bin/translation-extract -o lala;
BLA=`diff lala/recensio.pot src/recensio.translations/recensio/translations/locales/recensio.pot  | wc | sed -e 's/ *\([0-9]*\).*/\1/'`
echo $BLA "<= 4"
test $BLA -lt 5
