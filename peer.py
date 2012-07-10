#! /usr/bin/env python
# -*- coding: utf-8 -*-

from twisted.protocols.basic import NetstringReceiver
from twisted.internet.protocol import Factory, ClientFactory
from twisted.internet import reactor
from pydispatch import dispatcher

class ClipboardProtocol(NetstringReceiver):

	def __init__( self ):
		self.address = None

	def stringReceived( self, line ):
		dispatcher.send( signal='contents-received', sender=self.factory.peer, data=line )

	def makeConnection( self, transport ):
		NetstringReceiver.makeConnection( self, transport )
		address = transport.getPeer()
		self.address = address.host
		self.factory.peer.connections[self.address] = self

	def connectionLost( self, reason ):
		try:
			del self.factory.peer.connections[self.address]
		except KeyError:
			pass

class ClipboardProtocolServerFactory(Factory):
	protocol = ClipboardProtocol

	def __init__( self, peer ):
		self.peer = peer

class ClipboardProtocolClientFactory(ClientFactory):
	protocol = ClipboardProtocol

	def __init__( self, peer ):
		self.peer = peer

class ClipboardPeer(object):

	def __init__( self ):
		self.connections = {}

	def start( self ):
		reactor.listenTCP( 8123, ClipboardProtocolServerFactory( self ) )
		
	def connectTo( self, address ):
		if address not in self.connections:
			reactor.connectTCP( address, 8123, ClipboardProtocolClientFactory( self ) )

	def sendClipboardContents( self, data ):
		for address, protocol in self.connections.items():
			protocol.sendString( data )
