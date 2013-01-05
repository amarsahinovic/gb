#!/usr/bin/env python

"""gb (goto bookmark) is a simple bookmarks script for shell users.

Inspired by: http://bitbucket.org/sjl/t/

"""

from __future__ import print_function
import os
import sys
import random
import argparse


def _make_path(path):
    """Joins path, in case it consists of multiple parts (space in name)."""
    return ' '.join(path)


def _make_name(name):
    """Removes whitespace from bookmark name."""
    return name.replace(' ', '-')


def eprint(msg):
    """Shortcut to print(msg, file=sys.stderr).

    Printing to stderr needs to be done when using 'get' command and during
    initialization, so that we don't mess up the 'cd' command.

    For consistency, I print to stderr for error and notification messages, and
    I print to stdout when the output is usable to the caller ('get' command).

    """
    print(msg, file=sys.stderr)


class Bookmarks(object):
    """Contains user bookmarks.

    Bookmarks are read on startup, and are written back to file when a new
    bookmark is added or deleted.

    """
    def __init__(self):
        self.bookmarks = {}
        self.default_path = '.'
        self.bookmarks_file_dir = os.path.expanduser('~') + '/.b'
        self.bookmarks_file_path = self.bookmarks_file_dir + '/bookmarks'
        self.bookmarks_file = None
        self._init_bookmarks()
        self._load_bookmarks()

    def exit(self, reason=None):
        """Used to exit the program in a clean way.

        This way, 'cd' command is given the default_path and it executes
        normally, leaving the user in the current directory.

        """
        if reason:
            eprint(reason)
        print(self.default_path)
        sys.exit()

    def _init_bookmarks(self):
        """Checks for bookmarks directory and file, creating them if required.

        Terminates the program if an error occures during startup.

        """
        if not os.path.exists(self.bookmarks_file_dir):
            try:
                os.mkdir(self.bookmarks_file_dir)
            except OSError:
                self.exit('Unable to create bookmarks directory.')

        if not os.path.isdir(self.bookmarks_file_dir):
            self.exit('Bookmarks directory exists as file, exiting.')

        if os.path.isdir(self.bookmarks_file_path):
            self.exit('Bookmarks file is a directory, exiting.')

        if not os.path.exists(self.bookmarks_file_path):
            try:
                open(self.bookmarks_file_path, 'w').close()
            except IOError:
                self.exit('Unable to create bookmarks file.')

        try:
            self.bookmarks_file = open(self.bookmarks_file_path, 'r+')
        except IOError:
            self.exit("Unable to open bookmarks file.")

    def _load_bookmarks(self):
        """Loads bookmarks from file.

        Bookmarks are stored as lines in file as key value pairs. Key is the
        first word in line, and everything after that is path.

        """

        for line in self.bookmarks_file:
            parts = line.strip().split()
            if len(parts) < 2:
                continue
            name = parts.pop(0)
            path = _make_path(parts)
            self.bookmarks[name] = path

    def _save_bookmarks(self):
        """Saves bookmarks to file."""

        self.bookmarks_file.seek(0)

        for name, path in self.bookmarks.items():
            self.bookmarks_file.write("{0} {1}\n".format(name, path))

        self.bookmarks_file.truncate()
        self.bookmarks_file.close()

    def __getitem__(self, key):
        """Retrieves a single bookmark.

        The list itself will raise an exception if the bookmark is not found.

        """
        return self.bookmarks[key]

    def __setitem__(self, key, value):
        """Saves bookmark to to list and file.

        Since the program is designed to execute a single command every time
        it is run, it is ok to save bookmarks automatically.

        """
        self.bookmarks[key] = value
        self._save_bookmarks()

    def __delitem__(self, key):
        """Deletes a single bookmark.

        The list itself will raise an exception if the bookmark is not found.

        """
        del self.bookmarks[key]
        self._save_bookmarks()

    def __contains__(self, key):
        """Checks whether the bookmark is set."""
        return key in self.bookmarks

    def __len__(self):
        """Returns the number of stored bookmarks."""
        return len(self.bookmarks)

    def __repr__(self):
        """Returns the representation of bookmarks."""
        return repr(self.bookmarks)

    def __iter__(self):
        """Returns an iterator for bookmarks."""
        return iter(self.bookmarks)

    def nuke(self):
        """Nuke it from orbit.

        Deletes ALL stored bookmarks. Use with care.

        """
        self.bookmarks_file.seek(0)
        self.bookmarks_file.truncate()
        self.bookmarks_file.close()


def _make_parser():
    """Prepares and returns the parser."""
    parser = argparse.ArgumentParser(
        prog='b'
    )

    parser.add_argument('-v', help='verbose', action='store_true',
                        dest='verbose')

    subparsers = parser.add_subparsers(help='commands', dest='command')

    add_parser = subparsers.add_parser('add', help='Add (or update) bookmark')
    add_parser.add_argument('-u', help='Update bookmark', action='store_true', dest='update')
    add_parser.add_argument('name', nargs='?', default=os.path.split(os.getcwd())[-1],
                            help='bookmark name (current directory name if empty)')
    add_parser.add_argument('path', nargs='*', default=[os.getcwd()],
                            help='bookmark path (current path if empty)')

    get_parser = subparsers.add_parser('get', help='Get bookmark')
    get_parser.add_argument('name', default=None,
                            help='bookmark name', nargs='?')

    del_parser = subparsers.add_parser('del', help='Delete bookmark')
    del_parser.add_argument('name', help='bookamark name')

    list_parser = subparsers.add_parser('list', help='List bookmark(s)')
    list_parser.add_argument('name', help='bookmark name (list all if empty)', nargs='?')

    nuke_parser = subparsers.add_parser('nuke', help='nuke it from orbit (delete all)')
    nuke_parser.add_argument('--from-orbit', help="nuke location",
                             required=True, action="store_true")
    return parser


def _main():

    parser = _make_parser()
    args = parser.parse_args()

    # Prepare name and path (if any)
    try:
        args.name = _make_name(args.name)
    except AttributeError:
        pass

    try:
        args.path = _make_path(args.path)
    except AttributeError:
        pass

    if args.verbose:
        eprint(args)

    b = Bookmarks()

    if args.command == 'add':
        if args.name in b and not args.update:
            eprint('Bookmark exists. Use -u to update.')
        else:
            b[args.name] = args.path
            eprint('Bookmark saved.')

    elif args.command == 'get':
        if args.name is None:
            b.exit()
        try:
            print(b[args.name])
        except KeyError:
            b.exit('Bookmark not found.')

    elif args.command == 'del':
        try:
            del b[args.name]
            eprint('Bookmark deleted.')
        except KeyError:
            eprint('Bookmark not found.')

    elif args.command == 'list':
        for name in b:
            eprint("{0} {1}".format(name, b[name]))

    elif args.command == 'nuke':
        # Confirmation code required
        code = ''.join([str(random.randint(0, 9)) for x in range(0, 4)])
        confirm = input("Type {0} to confirm: ".format(code))
        if code == confirm:
            eprint('Launching nukes.')
            b.nuke()
        else:
            eprint('Launch aborted.')


if __name__ == '__main__':
    _main()
