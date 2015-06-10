# SecretKeeper
A single-file python 2 program that stores your secrets.

A program that opens a GUI text entry, and saves the encrypted data to itself. Windows takes issues with programs saving themselves, so this is Linux (possibly Mac) only for now.

To change the password (key), you must import from python, since I'm too lazy to make a GUI password changer at the moment:

    import SecretKeeper
    SecretKeeper.rekey('old_key', 'new_key')

To run, you can provide the password as an argument:

    ./SecretKeeper.py nicol

or, if you don't, a dialog will prompt you for the password.

TODO: I would like to keep this as pure python (no imports that don't ship with python / vanilla linux distros).
TODO: Improve the encryption. I don't think the XOR encryption is very strong.
