from ishmael import app

if __name__ == "__main__":
	# Flask debugger by default
	if app.debug: use_debugger = True
	
	try:
		# Use Eclipse / Aptana debugger (only config.ConfigPyDev sets this var to True)
		use_debugger = not(app.config.get('DEBUG_WITH_APTANA'))
	except:
		pass
	#use_debugger, use_reloader only active when debug=True
	app.run(debug=app.debug, use_debugger=use_debugger, use_reloader=use_debugger)
