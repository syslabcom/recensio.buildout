echo "" > ./stats.txt
cd src/recensio.translations

while :
do
  echo -n `git show --pretty=format:%ai HEAD | head -1 | sed -e "s/\+.*//" | sed -e 's/ /-/'` >> ../../stats.txt
  for i in de en fr
  do 
    echo -n " " `msgcmp recensio/translations/locales/$i/LC_MESSAGES/recensio.po recensio/translations/locales/recensio.pot 2>&1 | grep untranslated | wc -l` `grep msgid recensio/translations/locales/$i/LC_MESSAGES/recensio.po | wc -l` >> ../../stats.txt; 
  done
  echo "" >> ../../stats.txt; git checkout HEAD^ || break
done
git checkout master
cd ..
cd ..
