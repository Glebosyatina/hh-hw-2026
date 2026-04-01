from __future__ import annotations

from dataclasses import dataclass

from app.users import User
from app.users import LocalUser
from app.users import ForeignUser



LOCAL_PHONE_PREFIX = "+7"


@dataclass(slots=True)
class ActiveCall:
    caller: User
    receiver: User

    @property
    def is_cross_border(self) -> bool:
        return type(self.caller) is not type(self.receiver)


class Switchboard:
    def __init__(self) -> None:
        self._active_calls: list[ActiveCall] = []
        self._cross_border_calls = 0 #чтобы вычислять колво иногородних звонков

    #регистрация звонка
    def register_call(self, raw_call: str) -> ActiveCall:
        '''
        Метод должен принимать только 1 строку и возвращать класс ActiveCall.
        На входе строка должна быть вида "caller_id,caller_name,caller_phone,reciever_id,reciever_name,reciever_phone"

        Например: "1001,Иван Петров,+71234567890,1085,Адам Яковлев,+71255556666"
        '''

        #распарсить строку в два объекта LocalUser и ForeignUser
        #создать и добавить в лист ActiveCall
        params = raw_call.split(",")

        caller = None
        receiver = None

        #создаем callera и receivera
        if (params[2].startswith("+7")):
            caller = LocalUser(id=int(params[0]), fullname=params[1], phone=params[2])
        else:
            caller = ForeignUser(id=int(params[0]), fullname=params[1], phone=params[2])

        if (params[5].startswith("+7")):
            receiver = LocalUser(id=int(params[3]), fullname=params[4], phone=params[5])
        else:
           receiver = ForeignUser(id=int(params[3]), fullname=params[4], phone=params[5])

        #добавляем в лист активных звонков текущий вызов
        activeCall = ActiveCall(caller, receiver)
        if activeCall.is_cross_border:
            self._cross_border_calls += 1

        self._active_calls.append(activeCall)
        return activeCall

    #удаление звонка
    def unregister_call(self, call: ActiveCall):
        if call.is_cross_border:
            self._cross_border_calls -= 1
        self._active_calls.remove(call)

    def unregister_last_call(self):
        call = self._active_calls.pop()
        if call.is_cross_border:
            self._cross_border_calls -= 1


    def get_active_calls_count(self) -> int:
        return len(self._active_calls)

    def get_cross_border_calls_count(self) -> int:
        return self._cross_border_calls