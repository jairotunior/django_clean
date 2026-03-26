from django.contrib import admin

from .models import (
    Application,
    Position,
    Prospect,
    Requisition,
    RequisitionDetail,
)


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active", "id")
    list_filter = ("is_active",)
    search_fields = ("name", "description")


class RequisitionDetailInline(admin.TabularInline):
    model = RequisitionDetail
    extra = 0
    autocomplete_fields = ("position",)


@admin.register(Requisition)
class RequisitionAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active", "created_at", "updated_at", "id")
    list_filter = ("is_active", "created_at")
    search_fields = ("name", "description")
    readonly_fields = ("created_at", "updated_at")
    inlines = (RequisitionDetailInline,)


@admin.register(RequisitionDetail)
class RequisitionDetailAdmin(admin.ModelAdmin):
    list_display = ("requisition", "position", "is_active", "id")
    list_filter = ("is_active",)
    autocomplete_fields = ("requisition", "position")


@admin.register(Prospect)
class ProspectAdmin(admin.ModelAdmin):
    list_display = (
        "email",
        "first_name",
        "last_name",
        "user",
        "availability",
        "created_at",
        "id",
    )
    list_filter = ("availability", "created_at")
    search_fields = ("email", "first_name", "last_name", "phone", "city", "country")
    readonly_fields = ("created_at",)
    autocomplete_fields = ("user", "current_application")


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "prospect",
        "status",
        "requisition",
        "position",
        "availability",
        "created_at",
    )
    list_filter = ("status", "availability", "created_at")
    search_fields = (
        "id",
        "prospect__email",
        "prospect__first_name",
        "prospect__last_name",
    )
    readonly_fields = ("created_at",)
    autocomplete_fields = ("prospect", "requisition", "position")
