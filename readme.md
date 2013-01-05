Goto Bookmark
=============

Simple command-line directory bookmarks manager, inspired by http://bitbucket.org/sjl/t/

Setup instructions
------------------

1.) Clone the repo

2.) Edit your `.bashrc` or `.zshrc` and add the following:

    export GB_DIR=/path/to/gb
    source $GB_DIR/g.sh
    alias b=$GB_DIR/b.py

Replace `/path/to/gb` with real path to where you cloned this repo. 
Do not add trailing slash to the GB_DIR variable. You may need to login again to make this work.

Short usage instuctions
-----------------------

Use `b add` to save current directory to bookmarks with current directory name as the bookmark name.
Use `g name` to jump to that directory from any other directory.

Typical usage
-------------

For example, you have a project at some deeply nested location: `/home/username/projects/python/django/projectname/`

You go to the directory, and type `b add`

Next time, instead of typing `cd projects/python/django/projectname` you just type `g projectname` :)

Detailed usage instructions
---------------------------

Use `b -h` to get a list of commands.
Use `b COMMAND -h` to get help for specific command.

Use `b add` to add current directory to bookmarks. 
Bookmark name will be the same as the name of the current directory. 
If the bookmark with the same name already exists, it will __not__ be updated automatically.

Use `b add NAME` to save current directory under specified name.

Use `b add NAME PATH` to save custom path under specified name.

Use `add -u` command to update existing bookmark with new path. 
You can specify name and path if they are different from current path and directory name.

Use `b del NAME` to delete bookmark with specified name.

Use `b list` to list saved bookmarks.

Use `b nuke --from-orbit` to delete all bookmarks :)

Command `b get NAME` is not meant to be used directly, it is called from `g.sh` file.

Use `g NAME` to jump to the directory saved under the specified name.
