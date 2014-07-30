=========================
HTTP basic authentication
=========================

Sometimes you need to protect your site to only let certain people access it, whether it be for a staging site or a client preview or simply because you have personal information that you dont want just anyone to see.
Nacelle makes this really easy to do

Add the following to your user settings file::

		DISPATCHER_MODULE = 'nacelle.contrib.lockdown.dispatcher.lockdown_dispatcher'
		LOCKDOWN_USERNAME = 'foo'
		LOCKDOWN_PASSWORD = 'bar'
		LOCKDOWN_URL_EXCEPTIONS = []

While http basic authentication is handy for quickly restricting access to a site you should make use of the API's provided by App Engine for production sites.

In basic authentication, the username and password are transmitted as plain-text to the server. This makes basic authentication un-suitable for applications without SSL, as you would end up exposing sensitive passwords.