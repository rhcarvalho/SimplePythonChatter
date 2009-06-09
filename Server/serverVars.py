# -*- coding: utf-8 -*-
#APP VARIABLES
APP_NAME = "Simple Python Chatter Server"
APP_VERSION = "0.1"
LANG = 'pt-br'

#LOG Variables
LOG_INFO = 1
LOG_SEND = 2
LOG_RECV = 3
LOG_ERR = 4
LOG_CONN = 5
LOG_SERVER = 6

#BROADCAST Message variables
BROADCAST_EVERYBODY = 1
BROADCAST_CHAT = 2
BROADCAST_GAME = 3
BROADCAST_PM = 4

#PATHs
if LANG == 'pt-br':
    PATH_WELCOME_MSG = "serverData/welcome.msg.pt-br"
else:
    PATH_WELCOME_MSG = "serverData/welcome.msg"
PATH_DEFAULT_MAP_NAME = "Militia"
PATH_DEFAULT_MAP = "serverData/default.map"

def _(message):
    translations = {
"Established connection UID %s\n": u"Conexão estabelecida com UID %s\n",
"Currently there are %s users online and %s known users. %s Last user connected: %s (%s)": u"Existem %s usuários online e %s usuários conhecidos. %s Último usuário conectado: %s (%s)",
"Currently there are %s users online and %s known users. %s Last user disconnected: %s (%s)": u"Existem %s usuários online e %s usuários conhecidos. %s Último usuário desconectado: %s (%s)",
"Lost connection: \n": u"Conexão perdida: \n",
"Port:": u"Porta:",
"Welcome message:": u"Mensagem inicial:",
"Start Service": u"Iniciar Serviço",
"Browse": u"Procurar",
"Server options": u"Opções do Servidor",
"Log options": u"Opções de Log",
"Display options:": u"Opções de exibição:",
"Version ": u"Versão ",
"Attempting to start server at port ": u"Tentando iniciar servidor na porta ",
"Creating Factory": u"Iniciando Protocolo",
"Saving welcome message...": u"Salvando mensagem inicial...",
"Setting up Users datastructure": u"Configurando estrutura de usuários",
"Listening for incoming connections...": u"Aguardando conexões de entrada...",
}

    if LANG == 'pt-br':
        return translations.get(message, message)
    return message
