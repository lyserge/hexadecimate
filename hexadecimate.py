import argparse
import sys
import urllib2
import random
import string
import nltk
from nltk.corpus import stopwords
from nltk.corpus import wordnet
import html2text

parser = argparse.ArgumentParser(description='Text processing library for writers')

parser.add_argument('-f', '--file', nargs='?', type=argparse.FileType('r'),
                    help='a file to parse')
parser.add_argument('-o', '--outfile', nargs='?', type=argparse.FileType('w'),
                    default=sys.stdout, help='a file to write out to')
parser.add_argument('-u', '--url', help='a URL to parse')
parser.add_argument('--random', type=int, help='produce a list of random words (default 100 words)')
parser.add_argument('-r', '--rate', help='sample rate (default 16)', default=16, type=int)
parser.add_argument('-s', '--start', help='starting word index (default 0)', default=0, type=int)
parser.add_argument('--ignore-stopwords', action='store_true', default=False, help='ignore common words, e.g. in, or, but')
parser.add_argument('--ignore-proper', action='store_true', default=False, help='ignore proper nouns, i.e. those that begin with a capital letter')
#parser.add_argument('-m', '--mutate', action='store_true', default=False, help='mutate words')
#parser.add_argument('--mutate-rate', help='rate of mutation (default 8, i.e. one in every 8 words is mutated)', default=8, type=int)
parser.add_argument('--scramble', action='store_true', default=False, help='mix up the extracted words')

args = parser.parse_args()
source = ""

if args.file:
	source = args.file.read()
elif args.url:
	response = urllib2.urlopen(args.url)
	mime = response.info()['Content-Type']
	if ('text/plain' in mime):
		source = response.read()
	else:
		print "URL must be for a plain text document"
		sys.exit(1)
elif args.random:
	words = [line.strip() for line in open('words.txt')]
	random.shuffle(words)
	if args.ignore_stopwords:
		words = [word for word in words if word not in stopwords.words('english')]
	if args.ignore_proper:
		tagged = nltk.pos_tag(words)
		words = [tag[0] for tag in tagged if (tag[1]!='NNP' and tag[0] not in ["'s", "n't", "'m", "'ll", "'d"])]
		print words
else:
	parser.print_help()
	sys.exit(1)

if (not args.random) and (args.ignore_proper or args.ignore_stopwords):
	text = nltk.word_tokenize(source)
	tagged = nltk.pos_tag(text)
	if args.ignore_proper:
		tagged = [tag for tag in tagged if (tag[1]!='NNP' and tag[0] not in ["'s", "n't", "'m", "'ll", "'d"])]
	if args.ignore_stopwords:
		tagged = [tag for tag in tagged if tag[0] not in stopwords.words('english')]
	
	source = ' '.join([tag[0] for tag in tagged])	

if not args.random:
	source = source.translate(string.maketrans("",""), '!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~')
	words = source.split()
	hexadecimated = [words[i] for i in xrange(args.start, len(words), args.rate)]
	if args.scramble:
		random.shuffle(hexadecimated)
else:
	hexadecimated = words[:args.random]


hexadecimated = ' '.join(hexadecimated)

args.outfile.write(hexadecimated)
print ""
