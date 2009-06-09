# -*- coding: utf-8 -*-
#file clientVars.py

#Global Application Variables
APP_NAME = "Simple Python Chatter"
APP_VERSION = "0.1"

REACTOR_RUNNING = False
CHECK_FOR_MESSAGES_TO_SEND_TIMEOUT = 1

#LOG Variables
LOG_INFO = 1
LOG_SEND = 2
LOG_RECV = 3
LOG_ERR = 4
LOG_CONN = 5
LOG_SERVER = 6
LOG_MSG = 7
LOG_PM_RECV = 8
LOG_PM_SENT = 9

LANG = 'pt-br'

def _(message):
    translations = {
"You are connected to the server!\n": u"Você conectou ao servidor!\n",
"********** SERVER MESSAGE **********": u"******* MENSAGEM DO SERVIDOR *******",
"There are currently %s users online. This server had %s logins\n": u"Existem %s usuários online. Este servidor já recebeu %s logins.\n",
"********** JOINING CHAT **********": u"******** ENTRANDO NO CHAT ********",
"You've succesfully authenticated yourself on the server\n": u"Você foi autenticado no servidor com sucesso\n",
"%s joined the chat!": u"%s entrou no chat",
"%s left the premises": u"%s saiu do chat",
"\n\n===Lost connection to the server ===": u"\n\n=== Conexão com o servidor perdida ===",
"Couldn't connect...\n": u"Não foi possível conectar...\n",
}

    if LANG == 'pt-br':
        return translations.get(message, message)
    return message
