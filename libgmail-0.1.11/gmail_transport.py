#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------------
# Copyleft (K) by Jose Rodriguez. This source is free (GPL)
# Partially based on John Nielsen ASPN recipe (http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/301740)
# Partially based on Alessandro Budai recipe (http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/456195)
# ----------------------------------------------------------------------------------


# ClientCookie to connection through a proxy using the CONNECT method, (useful for SSL)
# tested with python 2.4

import mechanize as ClientCookie
import urllib
import httplib
import socket
import base64


def split_proxy_URL(proxy):
	if proxy is None:
	    return None, None, None

	try:
	    if proxy[:7] != 'http://':  # Ensures proxy string begins with 'http://'
	        proxy = 'http://' + proxy
	except:
	    pass

	proxy_username = proxy_password = None

	urltype, r_type = urllib.splittype(proxy)
	proxy, XXX = urllib.splithost(r_type)
	if '@' in proxy:
	    proxy_username, proxy = proxy.split('@', 1)
	    if ':' in proxy_username:
	        proxy_username, proxy_password = proxy_username.split(':', 1)

	return proxy, proxy_username, proxy_password



class ProxyHTTPConnection(httplib.HTTPConnection):

	_ports = {'http' : 80, 'https' : 443}

	def request(self, method, url, body=None, headers={}):
		#request is called before connect, so can interpret url and get
		#real host/port to be used to make CONNECT request to proxy
		proto, rest = urllib.splittype(url)
		if proto is None:
			raise ValueError, "unknown URL type: %s" % url

		host, rest = urllib.splithost(rest) # get host
		host, port = urllib.splitport(host) #try to get port

		#if port is not defined try to get from proto
		if port is None:
			try:
				port = self._ports[proto]
			except KeyError:
				raise ValueError, "unknown protocol for: %s" % url

		self._real_host = host
		self._real_port = port
		httplib.HTTPConnection.request(self, method, url, body, headers)
		

	def connect(self):
		httplib.HTTPConnection.connect(self)

		self.send("CONNECT %s:%d HTTP/1.0\r\n" % (self._real_host, self._real_port))
		if self.proxy_user is not None and self.proxy_passwd is not None:
			cred = base64.encodestring("%s:%s" % (urllib.unquote(self.proxy_user), urllib.unquote(self.proxy_passwd))).strip()
			self.send("Proxy-authorization: Basic %s\r\n" % cred)

		self.send("User-Agent: Mozilla/5.0 (Compatible; libgmail-python)\r\n\r\n")
		response = self.response_class(self.sock, strict=self.strict, method=self._method)
		(version, code, message) = response._read_status()
		#probably here we can handle auth requests...
		if code != 200:
			#proxy returned and error, abort connection, and raise exception
			self.close()
			raise socket.error, "Proxy connection failed: %d %s" % (code, message.strip())

		#eat up header block from proxy....
		while True:
			line = response.fp.readline() #should not use directly fp probablu
			if line == '\r\n': break


	@classmethod
	def new_auth(cls, proxy_host, proxy_user = None, proxy_passwd = None):
		cls.proxy_host = proxy_host
		cls.proxy_user = proxy_user
		cls.proxy_passwd = proxy_passwd

		return cls



class ProxyHTTPSConnection(ProxyHTTPConnection):
	
	default_port = 443

	def __init__(self, host, port = None, key_file = None, cert_file = None, strict = None):
		ProxyHTTPConnection.__init__(self, host, port)
		self.key_file = key_file
		self.cert_file = cert_file
	
	def connect(self):
		ProxyHTTPConnection.connect(self)
		#make the sock ssl-aware
		ssl = socket.ssl(self.sock, self.key_file, self.cert_file)
		self.sock = httplib.FakeSocket(self.sock, ssl)

		
class ConnectHTTPHandler(ClientCookie.HTTPHandler):

	def __init__(self, proxy=None, debuglevel=0):
		self.proxy, self.proxy_user, self.proxy_passwd = split_proxy_URL(proxy)
		ClientCookie.HTTPHandler.__init__(self, debuglevel)

	def do_open(self, http_class, req):
		if self.proxy is not None:
			req.set_proxy(self.proxy, 'http')
		return ClientCookie.HTTPHandler.do_open(self, ProxyHTTPConnection.new_auth(self.proxy, self.proxy_user, self.proxy_passwd), req)
	


class ConnectHTTPSHandler(ClientCookie.HTTPSHandler):

	def __init__(self, proxy=None, debuglevel=0):
		self.proxy, self.proxy_user, self.proxy_passwd = split_proxy_URL(proxy)
		ClientCookie.HTTPSHandler.__init__(self, debuglevel)

	def do_open(self, http_class, req):
		if self.proxy is not None:
			req.set_proxy(self.proxy, 'https')
		return ClientCookie.HTTPSHandler.do_open(self, ProxyHTTPSConnection.new_auth(self.proxy, self.proxy_user, self.proxy_passwd), req)


