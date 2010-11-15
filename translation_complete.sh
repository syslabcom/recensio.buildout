#!/bin/bash
mkdir lala; ./bin/translation-extract -o lala;test `diff lala/recensio.pot src/recensio.translations/recensio/translations/locales/recensio.pot  | wc | sed -e 's/ *\([0-9]*\).*/\1/'` -lt 5
