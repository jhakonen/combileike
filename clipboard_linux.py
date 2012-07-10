#! /usr/bin/env python
# -*- coding: utf-8 -*-

import gtk
from twisted.internet import reactor, task

class ClipboardImpl( object ):

	def __init__( self, publicImpl ):
		self.publicImpl = publicImpl
		self.contents = None
		self.clipboard = gtk.clipboard_get()
		self.loop = None

	def start( self ):
		if self.loop == None:
			# call GTK's event handling from twisted's reactor loop
			def processEvents():
				while gtk.events_pending():
					gtk.main_iteration( False )
			self.loop = task.LoopingCall( processEvents )
			self.loop.start( 0.1 )
			self.update()
		
	def onTextReceived( self, clipboard, text, data ):
		if text != '' and text != self.contents:
			self.contents = text
			self.publicImpl._notifyClipboardChange()
		# re-poll the contents again after 1 second
		reactor.callLater( 1.0, self.update )
	
	def update( self ):
		self.clipboard.request_text( self.onTextReceived )
	
	def stop( self ):
		if self.loop != None:
			self.loop.stop()
			self.loop = None

	def getClipboardContents( self ):
		return self.contents

	def setClipboardContents( self, data ):
		self.contents = data
		self.clipboard.set_text( data )
