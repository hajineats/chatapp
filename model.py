class Model():
    def __init__(self) -> None:
        # for 1:1 chat. key is sockname (recipient), list is the list of messages
        self.indiv_chat_dict: dict[str, list[str]] = {}

        # for group chat. key is group identifier
        self.group_chat_dict: dict[str, list[str]] = {}

    def add_indiv_message(self, sockname, message):
        # is this a new message?
        if sockname not in self.indiv_chat_dict:
            self.indiv_chat_dict[sockname] = []
        
        self.indiv_chat_dict[sockname].append(message)

    def get_indiv_message(self, sockname):
        if sockname not in self.indiv_chat_dict:
            return []
        return self.indiv_chat_dict[sockname]