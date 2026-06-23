from django.db import models


class Customer(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "customers"

    def __str__(self):
        return self.name


class Contact(models.Model):
    class Role(models.TextChoices):
        PRIMARY = "PRIMARY", "Primary"
        PURCHASE = "PURCHASE", "Purchase"
        SALES = "SALES", "Sales"
        LICENSE_HOLDER = "LICENSE_HOLDER", "License Holder"

    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="contacts"
    )
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=Role.choices)
    phone = models.CharField(max_length=50, blank=True)
    opt_in = models.BooleanField(default=False)
    opt_in_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} <{self.email}>"


class ImapAccount(models.Model):
    email_address = models.EmailField(unique=True)
    host = models.CharField(max_length=200)
    port = models.IntegerField(default=993)
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200, help_text="Encrypted at rest")
    use_ssl = models.BooleanField(default=True)
    last_sync = models.DateTimeField(null=True, blank=True)
    enabled = models.BooleanField(default=True)

    def __str__(self):
        return self.email_address


class Communication(models.Model):
    imap_account = models.ForeignKey(
        ImapAccount, on_delete=models.CASCADE, related_name="communications"
    )
    message_id = models.CharField(max_length=500, unique=True)
    from_address = models.EmailField()
    to_addresses = models.TextField()
    subject = models.CharField(max_length=500)
    body = models.TextField(blank=True)
    received_date = models.DateTimeField()
    raw_email = models.FileField(blank=True, upload_to="emails/")
    linked_to_contact = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-received_date"]

    def __str__(self):
        return f"{self.subject} - {self.from_address}"


class Attachment(models.Model):
    communication = models.ForeignKey(
        Communication, on_delete=models.CASCADE, related_name="attachments"
    )
    filename = models.CharField(max_length=500)
    content_type = models.CharField(max_length=200)
    file = models.FileField(upload_to="attachments/")
    parsed_text = models.TextField(blank=True)

    def __str__(self):
        return self.filename


class Purchase(models.Model):
    class Type(models.TextChoices):
        PRODUCT = "PRODUCT", "Product"
        SERVICE = "SERVICE", "Service"

    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="purchases"
    )
    type = models.CharField(max_length=10, choices=Type.choices, default=Type.PRODUCT)
    purchase_date = models.DateField()

    # Product-specific fields
    quote_file = models.CharField(
        max_length=500, blank=True,
        help_text="Path to quote PDF on OneDrive (e.g. OneDrive/EAxpertise/Quotes/...)",
        verbose_name="quote (PDF)"
    )
    invoice_file = models.CharField(
        max_length=500, blank=True,
        help_text="Path to invoice PDF on OneDrive (e.g. OneDrive/EAxpertise/Invoices/...)",
        verbose_name="invoice (PDF)"
    )

    # Service-specific fields
    service_name = models.CharField(max_length=200, blank=True, help_text="Name of the service (for Service-type purchases)")
    start_month = models.DateField(null=True, blank=True, help_text="Service start (set to 1st of month)")
    expiry_month = models.DateField(null=True, blank=True, help_text="Service expiry (set to last day of month) — signals renewal needed")

    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-purchase_date"]

    def __str__(self):
        if self.type == "SERVICE" and self.service_name:
            return f"Service: {self.service_name} ({self.customer.name})"
        return f"Purchase #{self.id} - {self.customer.name} ({self.purchase_date})"


class License(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="licenses"
    )
    purchase = models.ForeignKey(
        Purchase, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="licenses", help_text="Purchase that originated this license"
    )
    renewed_license = models.ForeignKey(
        "self", on_delete=models.SET_NULL, null=True, blank=True,
        related_name="renewals", help_text="Previous license this is a renewal of"
    )
    license_type = models.CharField(max_length=200, help_text="e.g. Sparx EA Corporate, Sparx EA Professional")
    start_date = models.DateField()
    expiry_date = models.DateField(help_text="Typically end of month")
    source_attachment = models.ForeignKey(
        Attachment, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="licenses", help_text="PDF/TXT document this license info was extracted from"
    )
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.license_type} ({self.customer.name})"

    class Meta:
        ordering = ["-start_date"]


class LicenseLineItem(models.Model):
    license = models.ForeignKey(
        License, on_delete=models.CASCADE, related_name="line_items"
    )
    description = models.CharField(max_length=500, help_text="Product or service name")
    is_service = models.BooleanField(default=False, help_text="Rented on 12-month basis")
    quantity = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        prefix = "[Service] " if self.is_service else ""
        return f"{prefix}{self.description} (x{self.quantity})"
