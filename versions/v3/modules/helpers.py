
import re
import threading
import json
import os
import os.path
import html
import hashlib
import operator
import uuid
import email
import copy
import io
import random
import base64
import requests
import pytz
import urllib3
import certifi
import inspect
import gc

UTF8 = "utf-8"

def md5(stringin=None):
	
	if (stringin == None):
		return None
	
	kpt1_ = hashlib.md5()
	kpt1_.update(stringin.encode(UTF8))
	return kpt1_.hexdigest()


def funcToVar():
	
	frame = inspect.currentframe()
	code  = frame.f_code
	globs = frame.f_globals
	functype = type(lambda: 0)
	funcs = []
	for func in gc.get_referrers(code):
		if type(func) is functype:
			if getattr(func, "__code__", None) is code:
				if getattr(func, "__globals__", None) is globs:
					funcs.append(func)
					if len(funcs) > 1:
						return None
	return funcs[0] if funcs else None


def checked(value=0):
	
	if (int(value) == 1):
		return "checked"
	return ""


def default(value, defaultval):
	if (value == None):
		return defaultval
	return value
