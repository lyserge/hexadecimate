import argparse
import sys
import urllib2

parser = argparse.ArgumentParser(description='Text processing library for writers')

parser.add_argument('-f', '--file', nargs='?', type=argparse.FileType('r'),
                    help='a file to parse')
parser.add_argument('-o', '--outfile', nargs='?', type=argparse.FileType('w'),
                    default=sys.stdout, help='a file to write out to')
parser.add_argument('-u', '--url', help='a URL to parse')
parser.add_argument('-r', '--rate', help='sample rate (default 16)', default=16, type=int)
parser.add_argument('-s', '--start', help='starting word index (default 0)', default=0, type=int)
parser.add_argument('--ignore-stopwords', action='store_true', default=False, help='ignore common words, e.g. in, or, but')
parser.add_argument('--ignore-proper', action='store_true', default=False, help='ignore proper nouns, i.e. those that begin with a capital letter')
parser.add_argument('-m', '--mutate', action='store_true', default=False, help='mutate words')
parser.add_argument('--mutate-rate', help='rate of mutation (default 8, i.e. one in every 8 words is mutated)', default=8, type=int)

args = parser.parse_args()
source = ""

if args.file:
	source = args.file.read()
elif args.url:
	response = urllib2.urlopen(args.url)
	source = response.read()

words = source.split()
hexadecimated = (words[i] for i in xrange(args.start, len(words), args.rate))
hexadecimated = ' '.join(hexadecimated)

args.outfile.write(hexadecimated)
