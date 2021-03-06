#!/bin/env python

import socket, re, shlex, operator

HOST = "localhost"
PORT = 6379

def get_parts(data):
    lexer = shlex.shlex(data, posix=True)
    lexer.whitespace_split = True
    return tuple(lexer)

def pub_all():
	print 'Publishing all'
	s.sendall('KEYS *\r\n')
	data = s.recv(1024)
	parts = get_parts(data)
	print parts
	keys = ()
	for i in range(len(parts)-3):
		if not ('*' in parts[i] or '$' in parts[i] or parts[i] is 'KEYS'):
			keys = (keys, parts[i])
	print keys
	normal(len(keys), keys)

def normal(cmd, args):
	if cmd is -1:
		cmd = len(args)
	for i in range(cmd):
		s.sendall('PUBLISH {0} UPDATE\r\n'.format(args[i]))

def special_bpop(cmd, args):
	print 'Special processing'
	normal(len(args)-1,args)

def special_flush(cmd, args):
	pub_all()
	pass

def special_mset(cmd, args):
	pass

def special_select(cmd, args):
	pub_all()
	pass

def special_shutdown(cmd, args):
	pass

def special_slave(cmd, args):
	pub_all()
	pass

def move():
	print('Moving')

red_mod_coms = {'APPEND':(1,normal),
		'BLPOP':(-1,special_bpop),
		'BRPOP':(-1,special_bpop),
		'BRPOPLPUSH':(2,normal),
		'DECR':(1,normal),
		'DECRBY':(1,normal),
		'DEL':(-1,normal),
		'FLUSHALL':(0,special_flush),
		'FLUSHDB':(0,special_flush),
		'GETSET':(1,normal),
		'HDEL':(1,normal),
		'HINCRBY':(1,normal),
		'HMSET':(1,normal),
		'HSET':(1,normal),
		'HSETNX':(1,normal),
		'INCR':(1,normal),
		'INCRBY':(1,normal),
		'LINSERT':(1,normal),
		'LPOP':(1,normal),
		'LPUSH':(1,normal),
		'LPUSHX':(1,normal),
		'LREM':(1,normal),
		'LSET':(1,normal),
		'LTRIM':(1,normal),
		'MOVE':(2,normal),
		'MSET':(-1,special_mset),
		'MSETNX':(-1,special_mset),
		'RENAME':(2,normal),
		'RENAMENX':(2,normal),
		'RPOP':(1,normal),
		'RPOPLPUSH':(2,normal),
		'RPUSH':(1,normal),
		'RPUSHX':(1,normal),
		'SADD':(1,normal),
		'SDIFFSTORE':(1,normal),
		'SELECT':(0,special_select),
		'SET':(1,normal),
		'SETBIT':(1,normal),
		'SETEX':(1,normal),
		'SETNX':(1,normal),
		'SETRANGE':(1,normal),
		'SHUTDOWN':(0,special_shutdown),
		'SINTERSTORE':(1,normal),
		'SLAVEOF':(0,special_slave),
		'SMOVE':(2,normal),
		'SORT':(1,normal),
		'SPOP':(1,normal),
		'SREM':(1,normal),
		'SUNIONSTORE':(1,normal),
		'ZADD':(1,normal),
		'ZINCRBY':(1,normal),
		'ZINTERSTORE':(1,normal),
		'ZREM':(1,normal),
		'ZREMRANGEBYRANK':(1,normal),
		'ZREMRANGEBYSCORE':(1,normal),
		'ZUNIONSTORE':(1,normal)	}

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST,PORT))

s.sendall('MONITOR\r\n')
while True:
	data = s.recv(1024)
	print 'Rec:', repr(data)
	parts = get_parts(data)
	print parts
	if parts is None:
		continue
	if parts[1].upper() in red_mod_coms:
		red_mod_coms[parts[1].upper()][1](red_mod_coms[parts[1].upper()][0],parts[2:])

