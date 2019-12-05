#! /usr/bin/env python

import argparse
import logging
import os
import io
import sys
import enum

# constants
BASE = ('A', ord('A'))
MOD = 26

# globals
args = None
logging.basicConfig(format='[%(asctime)s] %(name)s %(levelname)s: %(message)s')
logger = logging.getLogger('RunningKeyCipher')

class Action(enum.Enum):
    ENCRYPT = 0
    DECRYPT = 1

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

def perform(action, inputStream, keyStream, outputStream):
    logger.debug(f'Selected BASE {BASE[0]}({BASE[1]})')
    while True:
        # next source character
        schar = inputStream.read(1)
        if not schar:
            # end of input
            logger.debug('Reached end of input source stream. Stopping...')
            return
        if not schar.isalpha():
            logger.debug(f'Ignoring source character: "{schar}"')
            continue
        logger.debug(f'Next source character: "{schar}"')
        # next key character
        kchar = keyStream.read(1)
        while not kchar.isalpha():
            logger.debug(f'Ignoring key character: "{kchar}"')
            kchar = keyStream.read(1)
        logger.debug(f'Next key character: "{kchar}"')
        if not kchar:
            logger.error("Key shorter than Source! Stopping.")
            return
        # capitalize characters
        schar, kchar = schar.upper(), kchar.upper()
        # ordinals of inputs
        schar_val, kchar_val = ord(schar), ord(kchar)
        # same for base character
        base, base_val = BASE
        shift = schar_val + kchar_val if action == Action.ENCRYPT else schar_val - kchar_val
        # only for logging purposes
        operation = '+' if action == Action.ENCRYPT else '-'
        logger.debug(f'shift = {schar}({schar_val}) {operation} {kchar}({kchar_val}) = {shift}')
        # output character
        ochar_val = (MOD + shift) % MOD + base_val
        ochar = chr(ochar_val)
        logger.debug(f'({MOD} + {shift}) % {MOD} + {base}({base_val}) = {ochar}({ochar_val})')
        outputStream.write(ochar)

def main():
    args = get_arguments()
    if args.DEBUG:
        logger.setLevel(logging.DEBUG)
    action = Action.ENCRYPT if args.ACTION.upper() == 'ENCRYPT' else Action.DECRYPT
    perform(action, args.INPUT, args.KEY, args.OUTPUT)
    # new line for prettier console output
    args.OUTPUT.write('\n')
    # clean up
    args.INPUT.close()
    args.KEY.close()
    args.OUTPUT.close()

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
