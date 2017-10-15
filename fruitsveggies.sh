curl https://simple.wikipedia.org/wiki/List_of_fruits?action=raw | grep -Po  "\*+\[\[\K(\w*\s?\w*)" >> fruits.txt
curl https://simple.wikipedia.org/wiki/List_of_vegetables?action=raw | grep -Po "\*+\[\[\K(\w*\s?\w*)" >> vegetables.txt
