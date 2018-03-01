
import socket

class Chat ():
    def __init__ (self , host = socket . gethostname () , port =5000) :
         s = socket . socket ( type = socket . SOCK_DGRAM )
         s. settimeout (0.5)
         s. bind (( host , port ))
         self . __s = s