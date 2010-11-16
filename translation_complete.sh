#!/bin/bash
mkdir tmp_translations;
./bin/translation-extract -o tmp_translations;
grep msgid tmp_translations/recensio.pot | sort > tmp_translations/new.pot
grep msgid src/recensio.translations/recensio/translations/locales/recensio.pot | sort > tmp_translations/current.pot
BLA=`diff tmp_translations/new.pot tmp_translations/current.pot | wc | sed -e 's/ *\([0-9]*\).*/\1/'`
diff tmp_translations/new.pot tmp_translations/current.pot
test $BLA -lt 1
