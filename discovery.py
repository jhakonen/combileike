#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Transpyre
# Network File Transfer Program

from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor
from twisted.application.internet import MulticastServer
from twisted.internet import task
import socket
from pydispatch import dispatcher

class DiscoveryProtocol(DatagramProtocol):
	def __init__(self, api):
		self.address = api.multicastAddress
		self.port = api.multicastPort
		self.notify = api.onClientFound

	def startProtocol(self):
		print 'Host discovery: listening'
		self.transport.joinGroup(self.address)
 
	def ping(self):
		message = socket.gethostname()
		self.transport.write(message, (self.address, self.port))

	def datagramReceived(self, datagram, address):
		# Check if we received a dgram from another Transpyre instance
		if datagram != socket.gethostname():
			self.notify(datagram, address[0])

class DiscoveryAPI(object):
	"""
	Can emit following signals:
	  - client-found
	"""
	
	
	def __init__(self):
		self.discovery = None
		self.refresh = None
		self.loopDelay = 10
		self.multicastAddress = None
		self.multicastPort = None

	def setMulticastAddress(self, address):
		self.multicastAddress = address

	def setMulticastPort(self, port):
		self.multicastPort = port

	def start(self):
		self.stop()
		self.discovery = DiscoveryProtocol(self)
		reactor.listenMulticast(self.multicastPort, self.discovery)
		self.refresh = task.LoopingCall(self.discovery.ping)
		self.refresh.start(self.loopDelay)

	def stop(self):
		self.discovery = None
		if self.refresh != None:
			self.refresh.stop()
		self.refresh = None

	def onClientFound(self, name, address):
		dispatcher.send( signal='client-found', sender=self, address=address, name=name )
