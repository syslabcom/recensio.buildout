echo "" > ./stats.txt
cd ../src/recensio.translations

while :
do
  echo -n `git show --pretty=format:%ai HEAD | head -1 | sed -e "s/\+.*//" | sed -e 's/ /-/'` >> ../../translation_stats/stats.txt
  for i in de en fr
  do 
    echo -n " " `msgcmp recensio/translations/locales/$i/LC_MESSAGES/recensio.po recensio/translations/locales/recensio.pot 2>&1 | grep untranslated | wc -l` `grep msgid recensio/translations/locales/$i/LC_MESSAGES/recensio.po | wc -l` >> ../../translation_stats/stats.txt; 
  done
  echo "" >> ../../translation_stats/stats.txt; git checkout HEAD^ || break
done
git checkout master
cd ..
cd ..
cd translation_stats
