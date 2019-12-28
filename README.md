# Running Key Cipher
This is a python implementation of the known Running Key Cipher. It can be used to encrypt/decrypt any length of alpha text with a running key (a key of the same length or longer). Any alpha text can be used as key, such as a book or a poem.

![](https://github.com/Adel-Wehbi/RunningKeyCipher/workflows/UnitTests/badge.svg)

## Usage
```
$ python runningkeycipher.py -h

usage: runningkeycipher.py [-h] -a {encrypt,decrypt} -i INPUT -k KEY [-o OUTPUT] [--debug]

Encrypts or decrypts alpha text using a provided Running Key.

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Output file. If file exists, it will be overwritten. If omitted, will output to
                        stdout.
  --debug               Include this flag to switch on debug output.

Required Arguments:
  -a {encrypt,decrypt}, --action {encrypt,decrypt}
                        The operation to perform.
  -i INPUT, --input INPUT
                        Input text to encrypt/decrypt. Accepts a path to a text file or the text string
                        itself. Required.
  -k KEY, --key KEY     Running Key Cipeher. Accepts a path to a text file or the key string itself. Has
                        to be longer than source text. Required.
```
## Example
We will be using Isaac Asimov's "The Last Question" as a running key. Its text can be found online, as it is in the open domain. I got mine from [here](https://www.multivax.com/last_question.html "here"). Omit the title and start at "The last question was asked for the first time, half in jest, on May 21, 2061..."

To encrypt:
```bash
$ python runningkeycipher.py -a encrypt -i 'THERE IS AS YET INSUFFICIENT DATA FOR A MEANINGFUL ANSWER' -k ./thelastquestion.txt 

MOICEALQMCWMQBFQFXIUSIQYRRMHJTZREXTVURNFFQIABAWK
```

To decrypt:
```bash
$ python runningkeycipher.py -a decrypt -i MOICEALQMCWMQBFQFXIUSIQYRRMHJTZREXTVURNFFQIABAWK -k ./thelastquestion.txt 

THEREISASYETINSUFFICIENTDATAFORAMEANINGFULANSWER
```

## Security
If you are planning to use this for serious means, don't.

But if you must, the only advice I can give is this: use a truly randomized key, not a natural language key.
Refer to [wikipedia's Security entry on the subject.](https://en.wikipedia.org/wiki/Running_key_cipher#Security "wikipedia's Security entry on the subject.")
