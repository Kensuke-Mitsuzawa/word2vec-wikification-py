wiki_node_disambiguation
- - -

# What's this ?

- You can run "Wikification" as easy as possible.
    - According to wikipedia, [Wikification](https://en.wikipedia.org/wiki/Wikification) is `in computer science, entity linking with Wikipedia as the target knowledge base`
- You can get disambiguated result with its score.

Please visit [Github page](https://github.com/Kensuke-Mitsuzawa/word2vec_wikification_py) also.
If you find any bugs and you report it to github issue, I'm glad.
Any pull-requests are welcomed.


# Requirement

- Python3.x (checked under )
    - I recommend to use "Anaconda" distribution.

# Setup

`python setup.py install`

## Get wikipedia entity vector model

Go to [this page](http://www.cl.ecei.tohoku.ac.jp/~m-suzuki/jawiki_vector/) and download model file from [here](http://www.cl.ecei.tohoku.ac.jp/~m-suzuki/jawiki_vector/entity_vector.tar.bz2).
Or run `download_model.sh`

## To those who uses interface.predict_japanese_wiki_names()

You're supposed to have mysql somewhere.

The step until using it.

1. start mysql server somewhere
2. download latest mysql dump files
3. initialize wikipedia database with mysql


To download wikipedia dump files, execute following commands

```
wget https://dumps.wikimedia.org/jawiki/latest/jawiki-latest-redirect.sql.gz
wget https://dumps.wikimedia.org/jawiki/latest/jawiki-latest-page.sql.gz
gunzip jawiki-latest-redirect.sql.gz
gunzip jawiki-latest-page.sql.gz
```

To initialize wikipedia database with mysql,

```
% CREATE DATABASE wikipedia;
% mysql -u [user_name] -p[password] wikipedia < jawiki-latest-redirect.sql
% mysql -u [user_name] -p[password] wikipedia < jawiki-latest-page.sql
```

# Change logs

- version0.1
    - released
    - It supports only Japanese wikipedia
