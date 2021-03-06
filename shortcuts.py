#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import csv
import posixpath
from pathlib import Path
from re import sub
from re import compile


# fishshortcuts = ""
qute_shortcuts = ""
ranger_shortcuts = ""
bash_shortcuts = ""
# zsh_shortcuts has the same syntax as bash_shortcuts
nautilus_shortcuts = ""

home = str(Path.home()) + "/"

ranger_location = home + ".config/ranger/rc.conf"
bash_location = home + ".bashrc"
zsh_location = home + ".zshrc"
qute_location = home + ".config/qutebrowser/config.py"
nautilus_location = home + ".config/gtk-3.0/bookmarks"


# These are the labels that demarcate where the shortcuts
# go in the config files.
beg = "# DO NOT DELETE LMAO\n"
end = "# DO NOT DELETE LMAO"


# First we open the list of folder shortcuts and go down each line adding each
# in the required syntax to each of the three configs:
with open(home+".config/Scripts/folders") as fold:
    for line in csv.reader(fold, dialect="excel-tab"):
        # Adds the ranger go, tab, move and yank commands:
        ranger_shortcuts += ("map g" + line[0]
                             + " cd " + line[1]
                             + "\n")

        ranger_shortcuts += ("map t" + line[0]
                             + " tab_new " + line[1]
                             + "\n")

        ranger_shortcuts += ("map m" + line[0]
                             + " shell mv %s " + line[1]
                             + "\n")

        ranger_shortcuts += ("map Y" + line[0]
                             + " shell cp -r %s " + line[1]
                             + "\n")

        # Adds the bash_shortcuts shortcuts:
        bash_shortcuts += ("alias " + line[0]
                           + "=\"cd " + line[1]
                           + " && ls -a\""
                           + "\n")

        # qutebrowser shortcuts:
        qute_shortcuts += ("config.bind(';" + line[0]
                           + "', 'set downloads.location.directory " + line[1]
                           + " ;; hint links download')"
                           + "\n")

        # nautilus bookmarks
        nautilus_shortcuts += ("file://" + posixpath.expanduser(line[1])
			   + "\n")


# Goes through the config file file and adds the shortcuts to both
# bash_shortcuts and ranger.
with open(home + ".config/Scripts/configs") as conf:
    for line in csv.reader(conf, dialect="excel-tab"):
        # fishshortcuts+=("alias "+line[0]+"=\"vim "+line[1]+"\"\n")
        # fishshortcuts+=("abbr --add "+line[0]+" \"vim "+line[1]+"\"\n")
        bash_shortcuts += ("alias " + line[0]
                           + "=\"vim " + line[1]
                           + "\""
                           + "\n")

        ranger_shortcuts += ("map " + line[0] + " shell vim " + line[1] + "\n")


def replaceInMarkers(text, shortcuts):
    markers = compile(beg+"(.|\s)*"+end)
    replacement = beg+shortcuts+end
    return sub(markers, replacement, text)


def writeShortcuts(location, shortcuts):
    with open(location, "r+") as input:
        final = ""
        final += input.read()
        final = replaceInMarkers(final, shortcuts)
        input.seek(0)
        input.write(final)
        input.truncate()


def main():
    writeShortcuts(ranger_location, ranger_shortcuts)
    writeShortcuts(bash_location, bash_shortcuts)
    writeShortcuts(zsh_location, bash_shortcuts)
    writeShortcuts(qute_location, qute_shortcuts)
    writeShortcuts(nautilus_location, nautilus_shortcuts)

if __name__ == '__main__':
    main()
