import pickle

from pueue.helper.socket import connectClientSocket


def commandFactory(state, params={}):
    instruction = {'mode': state}
    for key, value in params.items():
        instruction[key] = value
    return sendCommand(instruction)


def sendCommand(command):
    client = connectClientSocket()
    client.send(pickle.dumps(command, -1))
    answer = client.recv(1048576)
    response = pickle.loads(answer)
    client.close()
    return response


def executeAdd(command):
    command['mode'] = 'add'
    command['status'] = 'queued'
    command['returncode'] = ''
    command['path'] = '/tmp'
    sendCommand(command)


def executeSwitch(command):
    command['mode'] = 'switch'
    sendCommand(command)


def getStatus():
    status = sendCommand({'mode': 'status'})
    return status