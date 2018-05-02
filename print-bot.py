import discord
import urllib
import socket
import sys
import urllib.request

PRINTER_ADDRESS = "ip address"
PRINTER_PORT = 13376
TOKEN = "token"

client = discord.Client ()

def tl (msg):
	s = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
	s.connect ((PRINTER_ADDRESS, PRINTER_PORT))
	s.send (msg)
	b = bytearray ([0x1B, 0x64, 0x01])
	s.send (b)
	s.close ()

def qr (msg):
	s = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
	s.connect (("37.136.101.54", 13376))
	b = bytearray ([0x1D, 0x28, 0x6B, 0x04, 0x00, 0x31, 0x41, 0x31, 0x00])
	s.send (b)

	b = bytearray ([0x1D, 0x28, 0x6B, 0x03, 0x00, 0x31, 0x43, 0x06])
	s.send (b)

	b = bytearray ([0x1D, 0x28, 0x6B, 0x03, 0x00, 0x31, 0x45, 0x33])
	s.send (b)

	data = msg.encode ()
	l = len (data) + 3
	pL = (l) % 256
	pH = int((l - pL) / 256)
	b = bytearray ([0x1D, 0x28, 0x6B, pL, pH, 0x31, 0x50, 0x30])
	s.send (b)
	s.send (data)

	b = bytearray ([0x1D, 0x28, 0x6B, 0x03, 0x00, 0x31, 0x51, 0x30])
	s.send (b)
	s.close ()
	cut ()

def cut ():
	s = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
	s.connect (("37.136.101.54", 13376))
	b = bytearray ([0x1B, 0x64, 0x06, 0x1D, 0x56, 0x01])
	s.send (b)
	s.close ()

def get_data (url):
	data = urllib.request.urlopen (url).read ()
	if len (data) > 0:
		cut ()
		tl (data)
		cut ()
	

@client.event
async def on_message (message):
	if message.author == client.user:
		return

	if message.content.startswith ('!hello'):
		msg = 'Why you so mean {0.author.name}?'.format (message)
		await client.send_message (message.channel, msg)

	elif message.content.startswith ('!google '):
		msg = 'https://google.com/?q=' + urllib.parse.quote_plus (message.content [8:])
		await client.send_message (message.channel, msg)

	elif message.content.startswith ('!cut'):
		cut ()

	elif message.content.startswith ('!qr'):
		msg = message.content[3:]
		if len (msg) > 0:
			qr (msg)

	elif message.content.startswith ('!url'):
		msg = message.content[4:]
		if len (msg) > 0:
			get_data (msg)
	else:
		msg = message.content
		if len (msg) > 0:
			tl (("@" + message.author.name + ": " + msg).encode ())

	

@client.event
async def on_ready ():
	print ('Logged in as')
	print (client.user.name)
	print (client.user.id)
	print ('-------------')



client.run (TOKEN)   
