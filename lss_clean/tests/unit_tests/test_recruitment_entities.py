from __future__ import annotations
import pytest
from datetime import datetime, timedelta
from uuid import UUID, uuid4


from lss_clean.contexts.recruitment.domain.entities import (
    Application,
    Position,
    Prospect,
    Requisition,
    RequisitionDetail,
)
from lss_clean.contexts.recruitment.domain.enums import (
    ApplicationStatus,
    Availability,
    CountryName,
)
from lss_clean.contexts.recruitment.domain.exceptions import BusinessRuleViolation


@pytest.fixture
def sample_prospect() -> Prospect:
    return Prospect.create(
        first_name="Jane",
        last_name="Doe",
        email="jane@example.com",
        phone="+1234567890",
        address="123 Main St",
        city="Bogotá",
        state="Cundinamarca",
        zip="110111",
        country=CountryName.COLOMBIA,
        user_id=1,
        availability=Availability.FULL,
    )


@pytest.fixture
def sample_requisition() -> Requisition:
    now = datetime.now()
    return Requisition(
        name="Engineering",
        description="Open roles",
        is_active=True,
        details=[],
        created_at=now,
    )


@pytest.fixture
def sample_position() -> Position:
    return Position(
        name="Developer",
        description="Backend",
        is_active=True,
    )


class TestProspectCreate:
    def test_create_returns_prospect_with_expected_fields(self) -> None:
        p = Prospect.create(
            first_name="A",
            last_name="B",
            email="a@b.com",
            phone="1",
            address="addr",
            city="city",
            state="st",
            zip="z",
            country=CountryName.MEXICO,
            user_id=1,
            availability=Availability.FULL,
        )
        assert isinstance(p, Prospect)
        assert p.first_name == "A"
        assert p.last_name == "B"
        assert p.email == "a@b.com"
        assert p.country == CountryName.MEXICO
        assert p.id is None
        assert p.current_application is None
        assert p.user_id == 1
        assert p.availability == Availability.FULL
        assert p._events == []


class TestProspectProperties:
    def test_full_name(self, sample_prospect: Prospect) -> None:
        assert sample_prospect.full_name == "Jane Doe"

    def test_has_current_application_false(self, sample_prospect: Prospect) -> None:
        assert sample_prospect.has_current_application is False

    def test_has_current_application_true(
        self, sample_prospect: Prospect, sample_requisition: Requisition, sample_position: Position
    ) -> None:
        sample_prospect.profile(
            sample_requisition, sample_position, Availability.FULL
        )
        assert sample_prospect.has_current_application is True

    def test_can_be_profiled_when_no_application(self, sample_prospect: Prospect) -> None:
        assert sample_prospect.can_be_profiled is True

    def test_can_be_profiled_when_candidate(
        self, sample_prospect: Prospect, sample_requisition: Requisition, sample_position: Position
    ) -> None:
        sample_prospect.profile(
            sample_requisition, sample_position, Availability.FULL
        )
        assert sample_prospect.can_be_profiled is True

    def test_can_be_profiled_false_when_not_candidate(
        self, sample_prospect: Prospect, sample_requisition: Requisition, sample_position: Position
    ) -> None:
        sample_prospect.profile(
            sample_requisition, sample_position, Availability.FULL
        )
        assert sample_prospect.current_application is not None
        sample_prospect.current_application.status = ApplicationStatus.FIRST_INTERVIEW
        assert sample_prospect.can_be_profiled is False

    def test_can_be_reapplied_true_when_terminal_and_old_enough(
        self,
        sample_prospect: Prospect,
    ) -> None:
        now = datetime.now()
        app = Application(
            prospect_id=sample_prospect.id,
            status=ApplicationStatus.REJECTED,
            created_at=now - timedelta(days=91),
        )
        sample_prospect.current_application = app
        assert sample_prospect.can_be_reapplied is True

    def test_can_be_reapplied_false_when_not_terminal(
        self, sample_prospect: Prospect
    ) -> None:
        now = datetime.now()
        app = Application(
            prospect_id=sample_prospect.id,
            status=ApplicationStatus.CANDIDATE,
            created_at=now - timedelta(days=100),
        )
        sample_prospect.current_application = app
        assert sample_prospect.can_be_reapplied is False

    def test_can_be_reapplied_false_when_too_recent(
        self, sample_prospect: Prospect
    ) -> None:
        now = datetime.now()
        app = Application(
            prospect_id=sample_prospect.id,
            status=ApplicationStatus.WITHDRAWN,
            created_at=now - timedelta(days=30),
        )
        sample_prospect.current_application = app
        assert sample_prospect.can_be_reapplied is False


class TestProspectProfile:
    def test_profile_raises_when_cannot_be_profiled(
        self,
        sample_prospect: Prospect,
        sample_requisition: Requisition,
        sample_position: Position,
    ) -> None:
        sample_prospect.profile(
            sample_requisition, sample_position, Availability.FULL
        )
        assert sample_prospect.current_application is not None
        sample_prospect.current_application.status = ApplicationStatus.APPROVED
        with pytest.raises(BusinessRuleViolation, match="cannot be profiled"):
            sample_prospect.profile(
                sample_requisition, sample_position, Availability.OVN
            )

    def test_profile_sets_application_and_appends_event(
        self,
        sample_prospect: Prospect,
        sample_requisition: Requisition,
        sample_position: Position,
    ) -> None:
        sample_prospect.profile(
            sample_requisition, sample_position, Availability.FULL_BD
        )
        assert sample_prospect.current_application is not None
        assert sample_prospect.current_application.status == ApplicationStatus.CANDIDATE
        assert sample_prospect.current_application.requisition == sample_requisition
        assert sample_prospect.current_application.position == sample_position
        assert sample_prospect.current_application.availability == Availability.FULL_BD


class TestApplication:
    def test_can_be_rejected_true_for_non_terminal(self) -> None:
        prospect = Prospect.create(
            first_name="X",
            last_name="Y",
            email="x@y.com",
            phone="1",
            address="a",
            city="c",
            state="s",
            zip="z",
            country=CountryName.COLOMBIA,
            user_id=1,
            availability=Availability.FULL,
        )
        app = Application(
            prospect_id=prospect.id,
            status=ApplicationStatus.CANDIDATE,
            created_at=datetime.now(),
        )
        assert app.can_be_rejected() is True

    def test_can_be_rejected_false_for_terminal(self) -> None:
        prospect = Prospect.create(
            first_name="X",
            last_name="Y",
            email="x@y.com",
            phone="1",
            address="a",
            city="c",
            state="s",
            zip="z",
            country=CountryName.COLOMBIA,
            user_id=1,
            availability=Availability.FULL,
        )
        app = Application(
            prospect_id=prospect.id,
            status=ApplicationStatus.REJECTED,
            created_at=datetime.now(),
        )
        assert app.can_be_rejected() is False

    def test_reject_sets_status_and_records_event(self) -> None:
        prospect = Prospect.create(
            first_name="X",
            last_name="Y",
            email="x@y.com",
            phone="1",
            address="a",
            city="c",
            state="s",
            zip="z",
            country=CountryName.COLOMBIA,
            user_id=1,
            availability=Availability.FULL,
        )
        app = Application(
            prospect_id=prospect.id,
            status=ApplicationStatus.CANDIDATE,
            created_at=datetime.now(),
        )
        app.reject(reason="Not a fit", notes="See HR")
        assert app.status == ApplicationStatus.REJECTED
        assert len(app._events) == 1
        assert app._events[0].reason == "Not a fit"
        assert app._events[0].notes == "See HR"

    def test_reject_raises_when_already_terminal(self) -> None:
        prospect = Prospect.create(
            first_name="X",
            last_name="Y",
            email="x@y.com",
            phone="1",
            address="a",
            city="c",
            state="s",
            zip="z",
            country=CountryName.COLOMBIA,
            user_id=1,
            availability=Availability.FULL,
        )
        app = Application(
            prospect_id=prospect.id,
            status=ApplicationStatus.TERMINATED,
            created_at=datetime.now(),
        )
        with pytest.raises(BusinessRuleViolation, match="cannot be rejected"):
            app.reject(reason="x", notes="y")


class TestRequisitionGraph:
    def test_requisition_detail_links_requisition_and_position(
        self, sample_requisition: Requisition, sample_position: Position
    ) -> None:
        detail = RequisitionDetail(
            position=sample_position,
            is_active=True,
        )
        assert detail.position is sample_position
        sample_requisition.details.append(detail)
        assert detail in sample_requisition.details
