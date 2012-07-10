#! /usr/bin/env python
# -*- coding: utf-8 -*-

from pydispatch import dispatcher

class Clipboard( object ):
	def __init__( self ):
		self.impl = ClipboardImpl( self )
		self.impl.start()

	def getClipboardContents( self ):
		return self.impl.getClipboardContents()

	def setClipboardContents( self, data ):
		return self.impl.setClipboardContents( data )

	def _notifyClipboardChange( self ):
		dispatcher.send( signal='changed', sender=self )


import sys
if sys.platform.startswith( 'linux' ):
	from clipboard_linux import ClipboardImpl
elif sys.platform.startswith( 'win32' ):
	from clipboard_win32 import ClipboardImpl
else:
	raise NotImplementedError( "Unknown platform detected '%s', there is no clipboard implementation for this yet!" % sys.platform )
