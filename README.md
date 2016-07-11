# auto-hms

A collection of tools to automate doing things with Nottingham Hackspace HMS, in lieu of an API.

The tools uses robobrowser (Python browser automation library) to login to HMS and poke the website in just the right way.

There's practically no error handling besides sort-of checking that the browser has found the right page.

All tools are very brittle and will probably break if anything is changed in HMS.

requirements.txt has the module requirements for pip, but doesn't include luck, which you'll probably need as well.

You'll need to add your HMS username and password to your environment variables as HMS_USERNAME and HMS_PASSWORD.

## auto-lazor

Automates booking the Nottingham Hackspace laser

## auto-label 

Automates creating LPS projects and printing their labels
