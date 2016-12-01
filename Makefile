INSTALL_DIR:=$(shell pwd)/installation/

install_deps:

    wget -O ./bin/entity_vector.tar.bz2 http://www.cl.ecei.tohoku.ac.jp/~m-suzuki/jawiki_vector/entity_vector.tar.bz2
    bzip2 -dc ./bin/entity_vector.tar.bz2 | tar xvf -
    mv entity_vector ./bin
    