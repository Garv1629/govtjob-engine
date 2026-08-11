from app.db.models.user import User
from app.core.security import hash_password


def test_user_creation(db_session):
    user = User(
        email="test_candidate@govtjob-agent.ai",
        hashed_password=hash_password("Secret123!"),
        full_name="Test Candidate"
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    assert user.id is not None
    assert user.email == "test_candidate@govtjob-agent.ai"
    assert user.is_active is True
