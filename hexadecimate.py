import argparse
import sys
import urllib2
import random
import string
import HTMLParser
import numbers

try:
	import nltk
except ImportError:
	print "The NLTK library is required. Try running 'pip install nltk'."
	sys.exit(1)

def isnum(word):
	try:
		i = float(word)
		#print "'%s' is a number" % word
		return True	
	except ValueError, TypeError:
		#print "'%s' is not a number" % word
		return False
	
#try:
#	from nltk.corpus import wordnet
#except ImportError:
#	print "The NLTK wordnet corpus is required for xxx. Try running 'python -m nltk.downloader wordnet'."

parser = argparse.ArgumentParser(description='Text processing library for writers')

parser.add_argument('-f', '--file', nargs='?', type=argparse.FileType('r'),
                    help='a file to parse')
parser.add_argument('-o', '--outfile', nargs='?', type=argparse.FileType('w'),
                    default=sys.stdout, help='a file to write out to')
parser.add_argument('-u', '--url', help='a URL to parse')
parser.add_argument('--random', type=int, help='produce a list of random words (default 100 words)')
parser.add_argument('-r', '--rate', help='sample rate (default 16)', default=16, type=int)
parser.add_argument('-s', '--start', help='starting word index (default 0)', default=0, type=int)
parser.add_argument('-l', '--limit', help='limit to a given number of words', type=int)
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
	headers = {'User-Agent' : "Hexadecimate"}
	req = urllib2.Request(args.url, None, headers)
	response = urllib2.urlopen(req)

	mime = response.info()['Content-Type']
	if ('text/plain' in mime):
		source = response.read()
	elif ('text/html' in mime):
		h = HTMLParser.HTMLParser()
		document = response.read().decode('ascii','ignore')
		document = h.unescape(document)
		source = nltk.clean_html(document).encode('utf8')
	else:
		print "URL must be for an HTML or plain text document"
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
	try:
		text = nltk.word_tokenize(source)
		tagged = nltk.pos_tag(text)
	except ImportError:
		print "The numpy library is required for ignoring proper nouns. Try running 'pip install numpy'."
		sys.exit(1)
	except LookupError:
		print "You need an NLTK word tokenizer installed for ignoring proper nouns. Try running 'python -m nltk.downloader maxent_treebank_pos_tagger'."
		sys.exit(1)

	if args.ignore_proper:
		tagged = [tag for tag in tagged if (tag[1]!='NNP' and tag[0] not in ["'s", "n't", "'m", "'ll", "'d"])]

	source = ' '.join([tag[0] for tag in tagged])	

if not args.random:
	source = source.translate(string.maketrans("",""), '!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~')
	words = source.split()
	words = [word for word in words if not isnum(word)]

	if args.ignore_stopwords:
		try:
			from nltk.corpus import stopwords
			words = [word for word in words if word not in stopwords.words('english')]
		except LookupError:
			print "The NLTK stopwords corpus is required for ignoring stopwords. Try running 'python -m nltk.downloader stopwords'."
			sys.exit(1)
	
	if args.scramble:
		random.shuffle(words)
	
	if args.limit:
		limit = args.limit*args.rate
	else:
		limit = len(words)
		
	hexadecimated = [words[i] for i in xrange(args.start, limit, args.rate)]
else:
	hexadecimated = words[:args.random]


hexadecimated = ' '.join(hexadecimated)

args.outfile.write(hexadecimated)
print ""
