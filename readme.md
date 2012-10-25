Goto Bookmark
=============

Simple bookmarks for shell users, inspired by http://bitbucket.org/sjl/t/

Setup instructions
------------------

1.) Clone the repo

2.) Edit your `.bashrc` or `.zshrc` and add the following:

    export GB_DIR=/path/to/gb
    source $GB_DIR/g.sh
    alias b=$GB_DIR/b.py

Replace `/path/to/gb` with real path to where you cloned this repo. 
Do not add trailing slash to the GB_DIR variable.

Usage instructions
------------------

Use `b -h` to get a list of commands.
Use `b COMMAND -h` to get help for specific command.
Use `g NAME` to jump to the directory saved under the specified name.
