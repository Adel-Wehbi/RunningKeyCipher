#! /usr/bin/env python

import argparse
import logging
import os
import io
import sys

# constants
BASE = ('A', ord('A'))

# globals
args = None
logging.basicConfig(format='[%(asctime)s] %(name)s %(levelname)s: %(message)s')
logger = logging.getLogger('RunningKeyCipher')

def get_arguments():
    parser = argparse.ArgumentParser(description="Encrypts or decrypts alpha text using a provided Running Key.")
    required = parser.add_argument_group('Required Arguments')
    required.add_argument(
        '-a',
        '--action',
        dest='ACTION',
        choices=["encrypt", "decrypt"],
        required=True,
        help="The operation to perform."
    )
    required.add_argument(
        '-i', 
        '--input',
        dest="INPUT",
        type=eval_input,
        required=True,
        help="Input text to encrypt/decrypt. Pass a text file (with leading ./, if in current dir) or the text itself. Required."
    )
    required.add_argument(
        '-k',
        '--key',
        dest="KEY",
        type=eval_input,
        required=True,
        help="Running Key Cipeher. Pass a text file (with leading ./, if in current dir) or the key itself. Has to be longer than source text. Required."
    )
    parser.add_argument(
        '-o',
        '--output',
        dest="OUTPUT",
        type=argparse.FileType('w'),
        default=sys.stdout,
        help="Output file. If file exists, it will be overwritten. If omitted, will output to stdout."
    )
    parser.add_argument(
        '--debug',
        dest='DEBUG',
        action='store_true',
        help="Include this flag to switch on debug output."
    )
    return parser.parse_args()

def eval_input(arg):
    # if argument has a forward slash (or backward slash for windows), consider it a path
    if os.path.sep in arg:
        if not os.path.isfile(arg):
            raise argparse.ArgumentTypeError(f"{arg} file does NOT exist!")
        return open(arg, mode='r')
    return io.StringIO(arg)

def main():
    global args
    args = get_arguments()
    if args.DEBUG:
        logger.setLevel(logging.DEBUG)
    logger.debug(f'Selected BASE {BASE[0]}({BASE[1]})')
    while True:
        # next source character
        schar = args.INPUT.read(1)
        logger.debug(f'Next source character: "{schar}"')
        if not schar:
            # end of file
            logger.debug('Reached end of file. Stopping...')
            args.OUTPUT.write('\n')
            die()
        if not schar.isalpha():
            logger.debug(f'Ignoring source character: "{schar}"')
            continue
        # next key character
        kchar = args.KEY.read(1)
        while not kchar.isalpha():
            logger.debug(f'Ignoring key character: "{kchar}"')
            kchar = args.KEY.read(1)
        logger.debug(f'Next key character: "{kchar}"')
        if not kchar:
            logger.error("Key shorter than Source! Stopping.")
            die()
        args.OUTPUT.write(encrypt(schar, kchar) if args.ACTION == 'encrypt' else decrypt(schar, kchar))

def encrypt(schar, kchar):
    schar, kchar = schar.upper(), kchar.upper()
    schar_val, kchar_val = get_vals(schar, kchar)
    base, base_val = BASE
    result_val = (schar_val + kchar_val) % 26 + base_val
    result = chr(result_val)
    logger.debug(f'encrypting char: ({schar}({schar_val}) + {kchar}({kchar_val})) % 26 + {base}({base_val}) = {result}({result_val})')
    return result

def decrypt(schar, kchar):
    schar, kchar = schar.upper(), kchar.upper()
    schar_val, kchar_val = get_vals(schar, kchar)
    base, base_val = BASE
    result_val = (26 + (schar_val - kchar_val)) % 26 + base_val
    result = chr(result_val)
    logger.debug(f'encrypting char: (26 + ({schar}({schar_val}) - {kchar}({kchar_val})) % 26 + {base}({base_val}) = {result}({result_val})')
    return result

def get_vals(first, second):
    first_val = ord(first)
    second_val = ord(second)
    logger.debug(f'Ordinal of {first} is {first_val}')
    logger.debug(f'Ordinal of {second} is {second_val}')
    return first_val, second_val

def die():
    # clean up
    logger.debug('Cleaning up')
    args.INPUT.close()
    args.KEY.close()
    args.OUTPUT.close()
    sys.exit()

if __name__ == '__main__':
    main()
else:
    logger.warn("As of now, this script does NOT support imoprting!")
