from trinity.session import SessionContext, SessionStore


def test_session_contract_types_exist() -> None:
    assert SessionContext.__name__ == 'SessionContext'
    assert hasattr(SessionStore, 'start')
    assert hasattr(SessionStore, 'end')
