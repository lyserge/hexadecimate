# arguments:
# --file: file to parse
# --outfile: file to write output to
# --url: url to parse
# --rate: sample rate [default 16 i.e. every 16th word]
# --start: starting word position [default 1 i.e. the first word]
# --stopwords=[y|n]: whether to ignore stopwords [default n]
# --proper=[y|n]: whether to ignore proper nouns [default n]
# --mutate: alter words
# --mrate: rate of mutation [default 8 i.e. one in every 8 words]

import argparse
import sys

parser = argparse.ArgumentParser(description='Text processing library for writers')

parser.add_argument('-f', '--file', nargs='?', type=argparse.FileType('r'),
                    default=sys.stdin, help='a file to parse')
parser.add_argument('-o', '--outfile', nargs='?', type=argparse.FileType('w'),
                    default=sys.stdout, help='a file to write out to')
parser.add_argument('-u', '--url', help='a URL to parse')
parser.add_argument('-r', '--rate', help='sample rate (default 16)', default=16, type=int)
parser.add_argument('-s', '--start', help='starting word index (default 1)', default=1, type=int)
parser.add_argument('--ignore-stopwords', action='store_true', default=False, help='ignore common words, e.g. in, or, but')
parser.add_argument('--ignore-proper', action='store_true', default=False, help='ignore proper nouns, i.e. those that begin with a capital letter')
parser.add_argument('-m', '--mutate', action='store_true', default=False, help='mutate words')
parser.add_argument('--mutate-rate', help='rate of mutation (default 8, i.e. one in every 8 words is mutated)', default=8, type=int)

args = parser.parse_args()
