import uuid

from django.conf import settings
from django.db import models

from lss_clean.contexts.recruitment.domain.enums import ApplicationStatus, Availability
from apps.recruitment.choices import (
    APPLICATION_STATUS_CHOICES,
    AVAILABILITY_CHOICES,
)


class CommonConfig(models.Model):

    id = models.BigAutoField(primary_key=True)
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Position(CommonConfig):

    name = models.CharField(max_length=255)
    description = models.TextField()
    is_active = models.BooleanField(default=True)

    class Meta:
        app_label = "recruitment"

    def __str__(self) -> str:
        return self.name


class Requisition(CommonConfig):

    name = models.CharField(max_length=255)
    description = models.TextField()
    is_active = models.BooleanField(default=True)

    class Meta:
        app_label = "recruitment"

    def __str__(self) -> str:
        return self.name


class RequisitionDetail(CommonConfig):

    requisition = models.ForeignKey(
        Requisition,
        on_delete=models.CASCADE,
        related_name="details",
    )
    position = models.ForeignKey(
        Position,
        on_delete=models.PROTECT,
        related_name="requisition_details",
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        app_label = "recruitment"
        constraints = [
            models.UniqueConstraint(
                fields=["requisition", "position"],
                name="recruitment_reqdetail_requisition_position_uniq",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.requisition_id} → {self.position_id}"


class Prospect(CommonConfig):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="prospects",
        related_query_name="prospect",
    )
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=64)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=128)
    country = models.CharField(max_length=128)
    state = models.CharField(max_length=128, blank=True, null=True)
    zip = models.CharField(max_length=32, blank=True, null=True)
    availability = models.CharField(
        max_length=32,
        choices=AVAILABILITY_CHOICES,
        default=Availability.FULL.value,
    )
    current_application = models.OneToOneField(
        "Application",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="current_application",
    )

    class Meta:
        app_label = "recruitment"

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name} <{self.email}>".strip()


class Application(CommonConfig):

    prospect = models.ForeignKey(
        Prospect,
        on_delete=models.CASCADE,
        related_name="applications",
        db_column="prospect_id",
    )
    status = models.CharField(
        max_length=32,
        choices=APPLICATION_STATUS_CHOICES,
        default=ApplicationStatus.CANDIDATE.value,
    )
    requisition = models.ForeignKey(
        Requisition,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="applications",
        db_column="requisition_id",
    )
    position = models.ForeignKey(
        Position,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="applications",
        db_column="position_id",
    )
    availability = models.CharField(
        max_length=32,
        choices=AVAILABILITY_CHOICES,
        blank=True,
        null=True,
    )

    class Meta:
        app_label = "recruitment"

    def __str__(self) -> str:
        return f"Application {self.id} ({self.status})"
