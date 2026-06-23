from django.db import models


class NewsSource(models.Model):
    name = models.CharField(max_length=200)
    url = models.URLField(unique=True)
    enabled = models.BooleanField(default=True)

    class Meta:
        verbose_name = "news source"

    def __str__(self):
        return self.name


class Article(models.Model):
    source = models.ForeignKey(
        NewsSource, on_delete=models.CASCADE, related_name="articles"
    )
    newsletter = models.ForeignKey(
        "Newsletter",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="articles",
    )
    source_url = models.URLField(unique=True)
    heading = models.CharField(max_length=500)
    summary = models.TextField()
    body = models.TextField(blank=True)
    included = models.BooleanField(default=False)
    discovered_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.heading


class Newsletter(models.Model):
    class Status(models.TextChoices):
        DRAFT = "DRAFT", "Draft"
        REVIEW = "REVIEW", "Review"
        SENT = "SENT", "Sent"

    title = models.CharField(max_length=200, default="EAxNewsletter")
    subject = models.CharField(max_length=500)
    body_html = models.TextField(blank=True, help_text="HTML version of newsletter")
    body_text = models.TextField(blank=True, help_text="Plain text version")
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.DRAFT)
    created_date = models.DateTimeField(auto_now_add=True)
    sent_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.title} - {self.created_date.date()}"


class NewsletterContact(models.Model):
    newsletter = models.ForeignKey(
        Newsletter, on_delete=models.CASCADE, related_name="sendouts"
    )
    contact = models.ForeignKey(
        "contacts.Contact", on_delete=models.CASCADE, related_name="newsletter_sendouts"
    )
    sent_date = models.DateTimeField(auto_now_add=True)
    opened_date = models.DateTimeField(null=True, blank=True)
    bounced = models.BooleanField(default=False)

    class Meta:
        verbose_name = "newsletter contact"
        verbose_name_plural = "newsletter contacts"
        unique_together = ["newsletter", "contact"]

    def __str__(self):
        return f"{self.contact.email} - {self.newsletter}"
