#!/usr/bin/env python
# -*- coding: utf-8 -*-

##	Zeddy
##	Version: 2017-05-29
##	2012-2017 - gaissa <https://github.com/gaissa>

# import external modules
from BeautifulSoup import BeautifulSoup
from threading import Thread
import feedparser
import json
import os
import random
import socket
import sys
import time
import tweepy
import urllib2

# set the path for internal modules
from sys import path
path.append('./lib')

# import internal modules
import zascii
import zassume

# the thread(s) holder
threads = []

# the consumer key for Twitter API, http://apps.twitter.com
consumer_key = ''
consumer_secret = ''

# an access token for Twitter API, http://apps.twitter.com
access_token = ''
access_token_secret = ''

# authenticate Twitter
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# everything is here and messy...
def main():

	rops = 'http://rops.fi/index.php?option=' + \
		   'com_content&view=category&id=38&Itemid=' + \
		   '188&format=feed&type=rss'

	jr = 'http://rops.fi/index.php?option=' + \
		 'com_content&view=category&id=40&Itemid=' + \
		 '190&format=feed&type=rss'

	ff = 'http://futisforum2.org/index.php?action=.xml;type=rss2;boards=24;limit=255'

	ff_santa = 'http://futisforum2.org/index.php?action=.xml;type=rss2;boards=38;limit=255'	

	rfeed1 = 'http://www.suomifutis.com/tag/rops/feed/'

	rfeed2 = 'http://palloseura.blogspot.com/feeds/posts/default/?alt=rss'

	nextleaguegame = 'http://futisforum2.org/index.php?board=11.0'

	nextcupgame = 'http://futisforum2.org/index.php?board=57.0'

	# set and print bot title
	title = 'Zeddy'
	print '\n\n' + title
	print '=' * len(title), '\n'

	# set connection
	irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	# make default port (6667)
	network = raw_input(':SET NETWORK = ')
	port = input(':SET PORT = ')
	print
	chan = raw_input(':SET CHANNEL = ')

	# bot setup
	admins = ''
	#admins = 'nick!~nick@xxx.fi'
	bot_nick = 'Zeddy'
	bot_names = 'Zeddy Zeddy Zeddy :Zeddy'
	quit_message = 'RoPS o/'

	# connect
	try:
		print '\n:CONNECTING = ' + network, port, chan + '\n'
		irc.connect((network, port))
	except:
		print ':NETWORK ERROR', '\n'
		sys.exit(0)

	# default output encoding
	reload(sys)
	sys.setdefaultencoding('utf-8')

	# set (send) names for the bot
	irc.send('NICK ' + bot_nick + '\r\n')
	irc.send('USER ' + bot_names + '\r\n')

	# join the channel
	irc.send('JOIN ' + chan + '\r\n')

	# say hello message
	with open ('./dict/greet', 'r') as w:
		wordlist = w.readlines()

	hello = random.choice(wordlist)
	time.sleep(1)
	irc.send('PRIVMSG ' + chan + ' :' + hello + '\r\n')

########################################################################

	# define send1 (string)
	def send1(msg):

		irc.send('PRIVMSG ' + chan + ' :' + str(msg) + '\r\n')
		#print (':' + chan + ' :' + str(msg) + '\r\n')

	# check connection
	def connection():

		if data.find('PING') != -1:
			irc.send('PONG ' + data.split() [1] + '\r\n')

	# when a user joins the channel
	def join():

		if data.find('JOIN') != -1:
			time.sleep(1)
			send1('RoPS o/')

	# reconnect if kicked
	def reconnect():

		if data.find('KICK') != -1:
			irc.send('JOIN ' + chan + '\r\n')

	# ADMIN give channel operator status to <nick>
	def operator():

		#if data.find(admins + ' PRIVMSG ' + chan + ' :!op') != -1:
		if data.find(' PRIVMSG ' + chan + ' :!op') != -1:
			op = data.split(':!op')
			ops = op[1].strip()
			time.sleep(1)
			irc.send('MODE ' + str(chan) + ' +o ' + str(ops) + '\r\n')
			time.sleep(1)

	# ADMIN quit bot
	def quitbot():

		if data.find(' PRIVMSG ' + chan + ' :!bot quit') != -1:
			irc.send('QUIT :' + quit_message + '\r\n')
			print '\n:DISCONNECTING\n\n'
			time.sleep(1)
			sys.exit(0)

	def newsparser(a):

		for x in range(0, 5):
			send1("" + a.entries[x].title + "")
			send1(a.entries[x].link)
			time.sleep(1)

	def twitter():

		if data.find(' PRIVMSG ' + chan + ' :!jumalin') != -1:
			tweetlist = []
			limit = 5
			for status in tweepy.Cursor(api.user_timeline, id='jumalin', tweet_mode='extended').items(limit):

				if hasattr(status, 'retweeted_status'):
					tweetlist.append('RT @' + status.entities['user_mentions'][0]['screen_name'] + ': ' + status.retweeted_status.full_text)
					#print "===="
					#print status.entities['user_mentions'][0]['screen_name']
					#print "===="
				else:
					tweetlist.append(status.full_text)
					#print "===="
					#print status
					#print "===="

			for i in range(0, limit):
				send1("" + '@jumalin: ' + "" + tweetlist[i])
				time.sleep(3)

	def news():

		if data.find(' PRIVMSG ' + chan + ' :!u') != -1:
			
			#print 'jes'
			# RSS 1
			#a = feedparser.parse(rops)

			# RSS 2
			b = feedparser.parse(rfeed1)					

			#send1("" + a.entries[0].title + "")
			#send1(a.entries[0].link)
			#time.sleep(2)
			send1("" + b.entries[0].title + "")
			send1(b.entries[0].link)
			time.sleep(2)			

			send1("" + b.entries[1].title + "")
			send1(b.entries[1].link)
			time.sleep(2)			
						
			#print socket.getaddrinfo
			
			origGetAddrInfo = socket.getaddrinfo
			
			def getAddrInfoWrapper(host, port, family=0, socktype=0, proto=0, flags=0):
				return origGetAddrInfo(host, port, socket.AF_INET, socktype, proto, flags)

			# replace the original socket.getaddrinfo by version above
			socket.getaddrinfo = getAddrInfoWrapper
			
			#print socket.getaddrinfo
			
			# RSS 3
			try:
				c = feedparser.parse(rfeed2)
			except Exception, e:
				print e
				logging.error('Error while retrieving feed.')
				logging.error(e)
				logging.error(formatExceptionInfo(None))
				logging.error(formatExceptionInfo1())				
			
			socket.getaddrinfo = origGetAddrInfo			
			
			send1("" + c.entries[0].title + "")
			send1(c.entries[0].link)
			time.sleep(2)
			send1("" + c.entries[1].title + "")
			send1(c.entries[1].link)
			time.sleep(2)

		if data.find(' PRIVMSG ' + chan + ' :!rops') != -1:
			newsparser(feedparser.parse(rops))

		if data.find(' PRIVMSG ' + chan + ' :!junnut') != -1:
			newsparser(feedparser.parse(jr))

		if data.find(' PRIVMSG ' + chan + ' :!jala') != -1:

			a = feedparser.parse(ff)

			for x in range(0, 255):
				if 'rops' in str(a.entries[x].title).lower():
					send1("" + a.entries[x].title + "")
					send1(a.entries[x].link)

					########################
					# f = open('./data/test', 'w')
					# f.close()

					# soup = BeautifulSoup(urllib2.urlopen(a.entries[x].link))

					# #print soup

					# for link in soup.findAll("div", { "class" : "post" }):
					#	#reload(sys)
					#	#sys.setdefaultencoding('utf-8')
					#	f = open('./data/test', 'a')
					#	f.write(str(link))
					#	f.write('\n')
						#f.close()

					####################################################
					#f.close()
					break
					#time.sleep(2)
					
		if data.find(' PRIVMSG ' + chan + ' :!santa') != -1:

			a = feedparser.parse(ff_santa)

			for x in range(0, 255):
				if 'santa' in str(a.entries[x].title).lower():
					send1("" + a.entries[x].title + "")
					send1(a.entries[x].link)
					break

		# player RSS feeds
		if data.find(' PRIVMSG ' + chan + ' :!malinen') != -1:
			playerfeed('http://www.suomifutis.com/tag/malinen-juha/feed/')		

		if data.find(' PRIVMSG ' + chan + ' :!borre') != -1 or data.find(' PRIVMSG ' + chan + ' :!kokko') != -1:
			playerfeed('http://www.suomifutis.com/tag/kokko-aleksandr/feed/')

		#if data.find(' PRIVMSG ' + chan + ' :!olli') != -1:
			#playerfeed('http://www.suomifutis.com/tag/poylio-olli/feed/')
			
		if data.find(' PRIVMSG ' + chan + ' :!simo') != -1 or data.find(' PRIVMSG ' + chan + ' :!simppa') != -1:
			playerfeed('http://www.suomifutis.com/tag/roiha-simo/feed/')

		if data.find(' PRIVMSG ' + chan + ' :!okkonen') != -1:
			playerfeed('http://www.suomifutis.com/tag/okkonen-antti/feed/')

		if data.find(' PRIVMSG ' + chan + ' :!saksela') != -1:
			playerfeed('http://www.suomifutis.com/tag/saksela-janne/feed/')
			
		if data.find(' PRIVMSG ' + chan + ' :!epic') != -1:
			playerfeed('http://www.suomifutis.com/tag/saxman-ville/feed/')

		if data.find(' PRIVMSG ' + chan + ' :!japi') != -1:
			playerfeed('http://www.suomifutis.com/tag/lahdenmaki-jarkko/feed/')

		if data.find(' PRIVMSG ' + chan + ' :!piri') != -1:
			playerfeed('http://www.suomifutis.com/tag/pirinen-juha/feed/')
			
		if data.find(' PRIVMSG ' + chan + ' :!taylor') != -1 or  data.find(' PRIVMSG ' + chan + ' :!roope') != -1:
			playerfeed('http://www.suomifutis.com/tag/taylor-robert/feed/')
			
		if data.find(' PRIVMSG ' + chan + ' :!juuso') != -1:
			playerfeed('http://www.suomifutis.com/tag/hamalainen-juuso/feed/')

		if data.find(' PRIVMSG ' + chan + ' :!riku') != -1:
			playerfeed('http://www.suomifutis.com/tag/ricardo/feed/')

		#if data.find(' PRIVMSG ' + chan + ' :!muksu') != -1:
			#playerfeed('http://www.suomifutis.com/tag/makitalo-mika/feed/')
			
		#if data.find(' PRIVMSG ' + chan + ' :!tomer') != -1:
			#playerfeed('http://www.suomifutis.com/tag/chencinski-tomer/feed/')
			
		#if data.find(' PRIVMSG ' + chan + ' :!obi') != -1:
			#playerfeed('http://www.suomifutis.com/tag/obilor-friday/feed/')

	# player feeds
	def playerfeed(tag):

		t = feedparser.parse(tag)

		if len(t['entries']) > 3:
			max = 3
		else:
			max = len(t['entries'])

		for x in range(0, max):
			send1("" + t.entries[x].title + "")
			send1(t.entries[x].link)
			time.sleep(2)
			
	# COMMENT
	def convert(urldata, x, y):

		if len(urldata) < 1:
			send1('BASIC USAGE: !i <url> <x, y>')
		else:
			try:			
							
			#print socket.getaddrinfo
			
				origGetAddrInfo = socket.getaddrinfo
				
				def getAddrInfoWrapper(host, port, family=0, socktype=0, proto=0, flags=0):
					return origGetAddrInfo(host, port, socket.AF_INET, socktype, proto, flags)

				# replace the original socket.getaddrinfo by version above
				socket.getaddrinfo = getAddrInfoWrapper

				infile = './data/tempfile'
				outfile = './data/image.txt'
				resizefile = './data/resize.jpg'

				req = urllib2.Request(url=urldata)
				file = urllib2.urlopen(req)

				output = open(infile, 'wb')
				output.write(file.read())
				output.close()

				# Pass the dimensions x, y (the char count), input file,
				# output file.
				zascii.convert(x, y, infile, outfile, resizefile)

				f = open(outfile, "r")

				for ff in f:
					if any(ext in ff for ext in zascii.chars):
						send1(ff,)
						time.sleep(3.5)

				f.close()
				
				socket.getaddrinfo = origGetAddrInfo

			except ValueError:
				print "..."
			except urllib2.HTTPError, e:
				print(e.code)
			except urllib2.URLError, e:
				print(e.args)

	# Zeddy draws ascii...
	def zeddysay():

		r = random.choice(os.listdir("./img/ascii/"))

		with open ('./img/ascii/' + r, 'r') as f:
			lines = f.readlines()

		for x in range(0, len(lines)):

			if (x % 2 == 0):
				send1(lines[x])
				time.sleep(3)
			else:
				send1(lines[x])
				#send1('\x1b[34;1m' + lines[x])
				time.sleep(6)

	# guess a match result
	def guess():

		if data.find(' PRIVMSG ' + chan + ' :!palio') != -1:

			home = zassume.guesser(zassume.h)
			time.sleep(2)
			away = zassume.guesser(zassume.a)

			send1(str(home) + ' - ' + str(away))

	# fetch and parse next match
	def nextmatch(data):

		#print data
		
		f = open('./data/forum', 'w')
		f.close()

		soup = BeautifulSoup(urllib2.urlopen(data))

		for link in soup.findAll('a'):
			if 'rops' in str(link.contents).lower():
				#reload(sys)
				#sys.setdefaultencoding('utf-8')

				with open ('./data/forum', 'a') as f:
					f.write(str(link.string))
					f.write('\n')
					f.write(str(link.get('href')))
					f.write('\n\n')


	# read next match from a file
	def next():
		
		w = False

	# say hello message
		with open ('./data/forum', 'r') as f:
			lines = f.readlines()

		# Elokuu 2015 11 kaupunnia...
		dic = {
			'helsinki': ['helsinki', 'helsingin', 'hifk', 'klubi', 'hupiklupi', 'hupiklubi', 'hjk'],
			'tampere': ['ilves', 'tampereen', 'ipa', 'ilves'],
			'kemi': ['kemi', 'pskemi', 'kings', 'keps', 'kommarit'],
			'kuopio': ['kuopion', 'kuopio', 'kups', 'savolaiset'],
			#'kotka': ['kotka', 'kotkan', 'ktp', 'kooteepee', 'fcktp', 'ahtaajat'],			
			'lahti': ['lahti', 'lahden', 'lahi', 'fclahti'],
			'maarianhamina': ['ifkmariehamn', 'maarianhamina', 'maarianhaminan', 'mifk', 'milf', 'milffi'],
			#'pietarsaari': ['pietarsaari', 'pietarsaaren', 'jaro', 'ffjaro'],			
			'rovaniemi': ['asiakeskustelut|rops', 'lc:rops', 'rovaniemi', 'rovaniemen', 'rops', 'ropsi', 'napapiirin'],
			'seinäjoki': ['seinäjoki', 'seinäjoen', 'sjk', 'nottajoki', 'nottajoen'],
			'turku': ['turku', 'turun', 'inter', 'fcinter', 'internazionale'],
			'vaasa': ['vaasa', 'vaasan', 'vps', 'vepsu'],
			'vantaa': ['pk-35 vantaa', 'vantaa', 'pk-35', 'pk35', '35', 'peekoo']}

		# WEATHER STARTS
		weather = lines[0].strip().replace(' ', '').split('-')
		team = weather[0].lower()
		
		#print weather
		#print team

		match = ''

		for index, k in enumerate(dic.keys()):

			for i in dic[k]:

				if i == team:

					key = ""

					zip = k
					url = 'http://api.wunderground.com/api/' + key + '/geolookup/conditions/lang:FI/q/Finland/' + zip + '.json'
					f = urllib2.urlopen(url)

					json_string = f.read()
					parsed_json = json.loads(json_string)

					#print parsed_json

					city = parsed_json['location']['city']
					temp_c = parsed_json['current_observation']['temp_c']
					feel_temp = parsed_json['current_observation']['feelslike_c']
					hum = parsed_json['current_observation']['relative_humidity']
					wind = str(round(parsed_json['current_observation']['wind_kph'] / 3.6, 2)) + 'm/s '					

					match = city.upper() + ' => Nyt: ' + str(temp_c) + '°C | Tuntuu: ' + feel_temp + '°C, (kosteus ' + hum + ', tuuli ' + wind +')'
					w = True
					break

				else:
					pass
		#WEATHER ENDS
		
		send1("" + lines[0].strip() + "")
		
		if w == True:
			send1(match)
		
		send1(lines[1].strip())

	# COMMENT THIS
	def match(match):		
		
		temp = data.split(':!')		
	
		if len(temp[1]) == 3 or len(temp[1]) == 5:
			nextmatch(match)
			next()

########################################################################

	# while true, run the bot
	while True:
		data = irc.recv(4096)
		print data

		connection()
		join()
		reconnect()
		operator()
		quitbot()
		guess()
		news()
		twitter()

		# COMMENT THIS
		if data.find(' PRIVMSG ' + chan + ' :!i') != -1:

			u = data.split(':!i')
			url = u[1].strip()

			dim = u[1].split(' ')

			#send1(dim[1])
			#send1(u[1].split(' '))

			if len(dim) == 4:
				ss = Thread(target = convert, args=(dim[1], dim[2], dim[3].strip('\r\n')))
			else:
				ss = Thread(target = convert, args=(url, 120, 56))

			threads.append(ss)
			#print ss.isAlive()
			threads[-1].start()

		# COMMENT
		if data.find(' PRIVMSG ' + chan + ' :!zeddy') != -1:

			zz = Thread(target = zeddysay)
			threads.append(zz)

			#print zz.isAlive()
			threads[-1].start()
			#threads[0].join()
			
					
		# tell the next cup match
		if data.find(' PRIVMSG ' + chan + ' :!c') != -1:			
			match(nextcupgame)

		# tell the next league match
		if data.find(' PRIVMSG ' + chan + ' :!s') != -1:
			match(nextleaguegame)

		# does nothing much :D
		if data.find(admins + ' PRIVMSG ' + bot_nick + ' :!party') != -1:
			send1('\o/')

########################################################################

# run Zeddy
if __name__ == "__main__":
	main()
