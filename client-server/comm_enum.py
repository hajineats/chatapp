# {CENUM_START_OF_MESSAGE}{sep}{CENUM_CLIENT_CONFIG}{sep}{self.nickname}{sep}{self.s.getsockname()}


CENUM_START_OF_MESSAGE = "!@#*()"
sep = "<SEP>" 

# client sends this message at the start of connection
CENUM_CLIENT_CONFIG_len = 4
CENUM_CLIENT_CONFIG = "CLIENTCONFIG"
CENUM_CLIENT_CONFIG_NICKNAME = 2
CENUM_CLIENT_CONFIG_SOCKNAME = 3

# client sends message to an individual with this message
CENUM_INDIVIDUALMESSAGE_len = 5
CENUM_INDIVIDUALMESSAGE = "INDIVIDUAL_MESSAGE"
CENUM_INDIVIDUALMESSAGE_SENDER_SOCKET = 2
CENUM_INDIVIDUALMESSAGE_RECEIVER_SOCKET = 3
CENUM_INDIVIDUALMESSAGE_MESSAGE = 4


# client receives individual message
CENUM_RCV_INDIVIDUALMESSAGE_len = 4
CENUM_RCV_INDIVIDUALMESSAGE = CENUM_START_OF_MESSAGE+sep+"RECEIVE_INDIVIDUAL_MESSAGE"
CENUM_RCV_INDIVIDUALMESSAGE_SENDER_SOCKET = 2
CENUM_RCV_INDIVIDUALMESSAGE_MESSAGE = 3


