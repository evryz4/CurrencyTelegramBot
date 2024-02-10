from typing import Union, Any

from aiogram.filters import BaseFilter
from aiogram.types import Message

class InstanceFilter(BaseFilter):
    def __init__(self, *types: Any) -> None:
        self.types = types
    
    async def __call__(self, msg: Message) -> bool:
        if len(self.types) > 1 and len(self.types) == len(msg.text.split()[1:]):
            for i in range(len(msg.text.split()[1:])):
                data = msg.text.split()[1:][i]
                if data.isdigit():
                    data = int(msg.text.split()[1:][i])
                if not isinstance(data, self.types[i]):
                    return False
        elif len(self.types) == 1 and len(msg.text.split()) > 1:
            for i in msg.text.split()[1:]:
                if i.isdigit():
                    i = int(i)
                if not isinstance(i, self.types[0]):
                    return False
        else:
            return False
        return True
