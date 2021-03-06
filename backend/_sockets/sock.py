#!/usr/bin/env python

# WS server example that synchronizes state across clients

import asyncio
import json
import logging
import websockets

logging.basicConfig()

STATE = {"value": 0}

USERS = set()


def state_event():
	return json.dumps({"type": "state", **STATE})


def users_event():
	return json.dumps({"type": "users", "count": len(USERS)})


async def notify_state(message, notto = None):
	if USERS:  # asyncio.wait doesn't accept an empty list
		filtered_users = list(filter(lambda x: x!=notto , [user for user in USERS]))
		if len(filtered_users)!=0:
			await asyncio.wait([user.send(message) for user in filtered_users])


async def notify_users():
	if USERS:  # asyncio.wait doesn't accept an empty list
		message = users_event()
		await asyncio.wait([user.send(message) for user in USERS])


async def register(websocket):
	USERS.add(websocket)
	# await notify_users()


async def unregister(websocket):
	USERS.remove(websocket)
	# await notify_users()


async def counter(websocket, path):
	# name = await websocket.recv()
	# print(f"name = {name}")
	# register(websocket) sends user_event() to websocket
	await register(websocket)
	try:
		# await websocket.send(state_event())
		async for message in websocket:
			print(f"received message = {message}")
			await notify_state(message, notto = websocket)
	finally:
		await unregister(websocket)


start_server = websockets.serve(counter, "0.0.0.0", 5000)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()