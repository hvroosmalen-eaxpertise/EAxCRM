from django.contrib import admin
from .models import Customer, Contact, ImapAccount, Communication, Attachment, Purchase, License, LicenseLineItem


class ContactInline(admin.TabularInline):
    model = Contact
    extra = 0


class AttachmentInline(admin.TabularInline):
    model = Attachment
    extra = 0


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ["name", "updated_at"]
    search_fields = ["name"]
    inlines = [ContactInline]


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "role", "customer", "opt_in"]
    list_filter = ["role", "opt_in"]
    search_fields = ["name", "email"]


@admin.register(ImapAccount)
class ImapAccountAdmin(admin.ModelAdmin):
    list_display = ["email_address", "host", "enabled", "last_sync"]
    list_filter = ["enabled"]


@admin.register(Communication)
class CommunicationAdmin(admin.ModelAdmin):
    list_display = ["subject", "from_address", "received_date", "imap_account", "linked_to_contact"]
    list_filter = ["linked_to_contact", "imap_account"]
    search_fields = ["subject", "from_address"]
    inlines = [AttachmentInline]


@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    list_display = ["filename", "communication", "content_type"]
    search_fields = ["filename"]


class LicenseInline(admin.TabularInline):
    model = License
    extra = 0
    fields = ["license_type", "start_date", "expiry_date", "purchase"]


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ["id", "customer", "type", "purchase_date", "service_name", "expiry_month"]
    list_filter = ["type", "purchase_date"]
    search_fields = ["customer__name", "service_name"]
    fieldsets = [
        (None, {"fields": ["customer", "type", "purchase_date", "notes"]}),
        ("Product", {"fields": ["quote_file", "invoice_file"], "classes": ["collapse"]}),
        ("Service", {"fields": ["service_name", "start_month", "expiry_month"], "classes": ["collapse"]}),
    ]
    inlines = [LicenseInline]


class LicenseLineItemInline(admin.TabularInline):
    model = LicenseLineItem
    extra = 0


@admin.register(License)
class LicenseAdmin(admin.ModelAdmin):
    list_display = ["license_type", "customer", "purchase", "start_date", "expiry_date"]
    list_filter = ["license_type"]
    search_fields = ["license_type", "customer__name"]
    raw_id_fields = ["renewed_license"]
    inlines = [LicenseLineItemInline]


@admin.register(LicenseLineItem)
class LicenseLineItemAdmin(admin.ModelAdmin):
    list_display = ["description", "license", "is_service", "quantity"]
    list_filter = ["is_service"]
