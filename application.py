#! /usr/bin/env python
# -*- coding: utf-8 -*-

from discovery import DiscoveryAPI
from clipboard import Clipboard
from peer import ClipboardPeer
from twisted.internet import reactor
from pydispatch import dispatcher

def onClientFound( name, address ):
	global peer
	#print "Found client '%s' (address: %s)" % (name, address)
	peer.connectTo( address )

def onClipboardChanged():
	global clipboard
	global peer
	data = clipboard.getClipboardContents()
	print "Clipboard contains: %s" % data
	peer.sendClipboardContents( data )

def onClipboardDataReceived( data ):
	global clipboard
	print "Received from other peer following data: %s" % data
	clipboard.setClipboardContents( data )

api = DiscoveryAPI()
api.setMulticastAddress( '224.100.84.59' )
api.setMulticastPort( 8192 )
api.start()

clipboard = Clipboard()

peer = ClipboardPeer()
peer.start()

dispatcher.connect( sender=api, signal='client-found', receiver=onClientFound )
dispatcher.connect( sender=clipboard, signal='changed', receiver=onClipboardChanged )
dispatcher.connect( sender=peer, signal='contents-received', receiver=onClipboardDataReceived )

reactor.run()

