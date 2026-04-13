import pytest

from app.switchboard import Switchboard
from app.users import ForeignUser, LocalUser


def test_register_call_creates_local_and_foreign_users() -> None:
    switchboard = Switchboard()

    active_call = switchboard.register_call(
        "1,Ivan Ivanov,+79990000000,2,John Smith,+15551234567"
    )

    assert isinstance(active_call.caller, LocalUser)
    assert isinstance(active_call.receiver, ForeignUser)
    assert active_call.caller.id == 1
    assert active_call.receiver.id == 2


def test_register_call_counts_active_calls() -> None:
    switchboard = Switchboard()

    switchboard.register_call(
        "1,Ivan Ivanov,+79990000000,2,Petr Petrov,+78880000000"
    )
    switchboard.register_call(
        "3,John Smith,+15551234567,4,Jane Doe,+33123456789"
    )

    assert switchboard.get_active_calls_count() == 2


def test_register_call_counts_calls_between_local_and_foreign_users() -> None:
    switchboard = Switchboard()

    switchboard.register_call(
        "1,Ivan Ivanov,+79990000000,2,John Smith,+15551234567"
    )
    switchboard.register_call(
        "3,Petr Petrov,+78880000000,4,Maria Petrova,+79991112233"
    )
    switchboard.register_call(
        "5,Jane Doe,+33123456789,6,Alex Doe,+442012345678"
    )

    assert switchboard.get_active_calls_count() == 3
    assert switchboard.get_cross_border_calls_count() == 1


def test_unregister_call() -> None:
    switchboard = Switchboard()

    call1 = switchboard.register_call(
        "1,Chuck Norris,+79990000000,2,Kurt Cobain,+15551234567"
    )

    assert switchboard.get_cross_border_calls_count() == 1

    switchboard.unregister_call(call1)
    assert switchboard.get_cross_border_calls_count() == 0

    switchboard.register_call(
        "3,Jacque Fresco,+78880000000,4,Robert Oppenheimer,+79991112233"
    )
    switchboard.register_call(
        "5,Keanu Reeves,+33123456789,6,Thomas Hanks,+44201234567"
    )
    assert switchboard.get_active_calls_count() == 2

    switchboard.unregister_last_call()
    assert switchboard.get_active_calls_count() == 1

def test_incorrect_number() -> None:
    switchboard = Switchboard()

    call1 = switchboard.register_call(
        "1,Chuck Norris,blablabla,2,Kurt Cobain,bububu"
    )

    assert switchboard.get_active_calls_count() == 0

def test_incorrect_user() -> None:
    switchboard = Switchboard()

    call1 = switchboard.register_call(
        "1,Chuck Norris,+79990000000,2,user123,+44201234567"
    )
    call2 = switchboard.register_call(
            "1,Chuck Norris,+79990000000,2,user 123,+44201234567"
        )

    assert switchboard.get_active_calls_count() == 0

def test_incorrect_id() -> None:
    switchboard = Switchboard()

    call1 = switchboard.register_call(
        "1,Chuck Norris,+79990000000,-1,Adele,+44201234567"
    )

    assert switchboard.get_active_calls_count() == 0