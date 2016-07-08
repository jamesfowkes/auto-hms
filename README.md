# auto-lazor
A very brittle Python tool to automate booking the Nottingham Hackspace laser

In the absence of an API to allow using the booking tool, this uses robobrowser (Python browser automation library) to login to HMS and book the laser.

There's practically no error handling besides sort-of checking that the browser has found the right page.

requirements.txt has the module requirements for pip, but doesn't include luck, which you'll probably need as well.
