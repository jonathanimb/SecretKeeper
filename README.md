# SecretKeeper
A single-file python 2 program that stores your secrets.

A program that opens a GUI text entry, and saves the encrypted data to itself. Windows takes issues with programs saving themselves, so this is Linux (possibly Mac) only for now.

To change the password (key), you must import from python, since I'm too lazy to make a GUI password changer at the moment:

    import SecretKeeper
    SecretKeeper.rekey('old_key', 'new_key')

To run, you can provide the password as an argument:

    ./SecretKeeper.py nicol

or, if you don't, a dialog will prompt you for the password.

In my mind, I separate things by a blank line. Therefore searching for something displays everything after the found search term until a blank line is encountered.

After making changes, the Close button becomes a Save&Close button. If you don't want to save your changes, close with the OS (little x on the title bar, usually, or middle click on the Gnome panel).

