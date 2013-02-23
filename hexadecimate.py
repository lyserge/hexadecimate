# hexadecimate.py - Text processing library for writers
# Copyright (c) 2013 by lyserge (lyserge@gmail.com)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

version_info = """Hexadecimate 1.0.0"""

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
	
#try:
#	from nltk.corpus import wordnet
#except ImportError:
#	print "The NLTK wordnet corpus is required for xxx. Try running 'python -m nltk.downloader wordnet'."

try:
	import numpy
except ImportError:
	print "The numpy library is required. Try running 'pip install numpy'."
	sys.exit(1)

def isnum(word):
	try:
		i = float(word)
		return True	
	except ValueError, TypeError:
		return False
	
def getURL(url):
	try:
		headers = {'User-Agent' : "Hexadecimate"}
		req = urllib2.Request(url, None, headers)
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
	except:
		print "Bad URL provided"
		sys.exit(1)
		
	return source
	
def getRandom(ignore_stopwords, ignore_proper):
	words = [line.strip() for line in open('words.txt')]
	if ignore_stopwords:
		words = stripStop(words)
	if ignore_proper:
		words = stripProper(words)
	return words
	
def stripProper(source):
	try:
		if type(source) is str:
			text = nltk.word_tokenize(source)
		else:
			text = source
		tagged = nltk.pos_tag(text)
	except LookupError:
		print "You need an NLTK word tokenizer installed for ignoring proper nouns. Try running 'python -m nltk.downloader maxent_treebank_pos_tagger'."
		sys.exit(1)

	tagged = [tag[0] for tag in tagged if (tag[1]!='NNP' and tag[0] not in ["'s", "n't", "'m", "'ll", "'d"])]
	
	if type(source) is str:
		return ' '.join(tagged)
	else:
		return tagged

def stripStop(words):
	return [word for word in words if word.lower() not in stopwords.words('english')]

def getWords(source):
	source = source.translate(string.maketrans("",""), '!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~')
	words = source.split()
	words = [word for word in words if not isnum(word)]
	return words
	
def generateWords(source, length):
	text = nltk.Text(source.split())
	if '_trigram_model' not in text.__dict__:
		estimator = lambda fdist, bins: nltk.LidstoneProbDist(fdist, 0.2)
		text._trigram_model = nltk.NgramModel(3, text, estimator)
	return text._trigram_model.generate(length) 

parser = argparse.ArgumentParser(description='Text processing library for writers')

sources = parser.add_mutually_exclusive_group()
sources.add_argument('-f', '--file', nargs='?', type=argparse.FileType('r'),
                    help='a file to parse')
sources.add_argument('-u', '--url', help='a URL to parse')
sources.add_argument('--random', type=int, help='produce a list of random words (default 100 words)')

parser.add_argument('-o', '--outfile', nargs='?', type=argparse.FileType('w'),
                    default=sys.stdout, help='a file to write out to')
parser.add_argument('-r', '--rate', help='sample rate (default 16)', default=16, type=int)
parser.add_argument('-s', '--start', help='starting word index (default 0)', default=0, type=int)
parser.add_argument('-l', '--limit', help='limit to a given number of words', type=int)
parser.add_argument('--ignore-stopwords', action='store_true', default=False, help='ignore common words, e.g. in, or, but')
parser.add_argument('--ignore-proper', action='store_true', default=False, help='ignore proper nouns, i.e. those that begin with a capital letter')
#parser.add_argument('-m', '--mutate', action='store_true', default=False, help='mutate words')
#parser.add_argument('--mutate-rate', help='rate of mutation (default 8, i.e. one in every 8 words is mutated)', default=8, type=int)
parser.add_argument('--scramble', action='store_true', default=False, help='mix up the extracted words')
parser.add_argument('-g', '--generate', type=int, help='generate random sentences inspired by the source text')
parser.add_argument('-v', '--version', action='version', version=version_info)

args = parser.parse_args()
source = ""

if args.ignore_stopwords:
	try:
		from nltk.corpus import stopwords
	except LookupError:
		print "The NLTK stopwords corpus is required for ignoring stopwords. Try running 'python -m nltk.downloader stopwords'."
		sys.exit(1)

if args.file:
	source = args.file.read()
elif args.url:
	source = getURL(args.url)
elif args.random:
	words = getRandom(args.ignore_stopwords, args.ignore_proper)
else:
	parser.print_help()
	sys.exit(1)


if args.generate:
	if (args.rate != 16) or (args.start != 0) or args.limit or args.random or args.ignore_proper or args.ignore_stopwords or args.scramble:
		print "The following options cannot be used in conjunction with -g: -r, -s, -l, --random, --ignore-proper, --ignore-stopwords, --scramble"
		sys.exit(1)
	hexadecimated = generateWords(source, args.generate)
elif args.random:
	random_indices = numpy.random.randint(0, len(words), args.random)
	hexadecimated = [words[random_index] for random_index in random_indices]
else:
	if args.ignore_proper:
		source = stripProper(source)
	
	words = getWords(source)
	
	if args.ignore_stopwords:
		words = stripStop(words)
	
	if args.scramble:
		random.shuffle(words)
	
	if args.limit:
		limit = args.limit*args.rate
	else:
		limit = len(words)
		
	hexadecimated = [words[i] for i in xrange(args.start, limit, args.rate)]

if type(hexadecimated) is list:
	hexadecimated = ' '.join(hexadecimated)
args.outfile.write(hexadecimated)

print ""
