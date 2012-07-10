#! /usr/bin/env python
# -*- coding: utf-8 -*-

import win32gui, win32api, win32con
from ctypes import *
import sys
from twisted.internet import task

WM_CLIPBOARDUPDATE = 0x031D

class ClipboardImpl(object):

	def __init__(self, publicImpl):
		self.publicImpl = publicImpl

	def start(self):
		self.lastSequenceNumber = -1
		win32gui.InitCommonControls()
		self.hinst = win32api.GetModuleHandle(None)
		className = 'MyWndClass'
		message_map = {
			WM_CLIPBOARDUPDATE: self.onClipboardUpdate,
			win32con.WM_DESTROY: self.OnDestroy
		}
		wc = win32gui.WNDCLASS()
		wc.style = win32con.CS_HREDRAW | win32con.CS_VREDRAW
		wc.lpfnWndProc = message_map
		wc.lpszClassName = className
		win32gui.RegisterClass(wc)
		style = win32con.WS_OVERLAPPEDWINDOW
		self.hwnd = win32gui.CreateWindow(
			className,
			'My win32api app',
			style,
			win32con.CW_USEDEFAULT,
			win32con.CW_USEDEFAULT,
			300,
			300,
			0,
			0,
			self.hinst,
			None
		)
		win32gui.UpdateWindow( self.hwnd )
		#win32gui.ShowWindow(self.hwnd, win32con.SW_SHOW)
		windll.user32.AddClipboardFormatListener( self.hwnd )

		self.loop = task.LoopingCall( win32gui.PumpWaitingMessages )
		self.loop.start( 1.0 )
		

	def stop(self):
		if self.loop != None:
			self.loop.stop()
			self.loop = None

	def getClipboardContents(self):
		result = None
		if windll.user32.IsClipboardFormatAvailable( win32con.CF_TEXT ) != 0:
			if windll.user32.OpenClipboard( self.hwnd ) == 0:
				raise Exception("Failed to open the clipboard!")
			memoryObjectHandle = windll.user32.GetClipboardData( win32con.CF_TEXT )
			if memoryObjectHandle:
				contentsPointer = windll.kernel32.GlobalLock( memoryObjectHandle )
				if contentsPointer:
					result = c_char_p( contentsPointer ).value
					windll.kernel32.GlobalUnlock( memoryObjectHandle )
			windll.user32.CloseClipboard()
		return result
		
	def setClipboardContents( self, data ):
		if windll.user32.OpenClipboard( self.hwnd ) == 0:
			raise Exception("Failed to open the clipboard!")
		memoryObjectHandle = windll.kernel32.GlobalAlloc( win32con.GMEM_MOVEABLE, len(data) + 1 )
		if memoryObjectHandle:
			contentsPointer = windll.kernel32.GlobalLock( memoryObjectHandle )
			memmove( contentsPointer, data, len(data) + 1 )
			windll.kernel32.GlobalUnlock( memoryObjectHandle )
			
			windll.user32.EmptyClipboard()
			windll.user32.SetClipboardData( win32con.CF_TEXT, memoryObjectHandle )
		windll.user32.CloseClipboard()
		self.lastSequenceNumber = windll.user32.GetClipboardSequenceNumber()

	def OnDestroy( self, hwnd, message, wparam, lparam ):
		self.stop()
		return True

	def onClipboardUpdate( self, hwnd, message, wparam, lparam ):
		sequenceNumber = windll.user32.GetClipboardSequenceNumber()
		if self.lastSequenceNumber < sequenceNumber:
			self.lastSequenceNumber = sequenceNumber
			self.publicImpl._notifyClipboardChange()
		return True
