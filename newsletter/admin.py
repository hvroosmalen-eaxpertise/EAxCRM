from django.contrib import admin
from .models import NewsSource, Article, Newsletter, NewsletterContact


class ArticleInline(admin.TabularInline):
    model = Article
    extra = 0
    fields = ["source_url", "heading", "included"]


class NewsletterContactInline(admin.TabularInline):
    model = NewsletterContact
    extra = 0
    readonly_fields = ["sent_date", "opened_date", "bounced"]


@admin.register(NewsSource)
class NewsSourceAdmin(admin.ModelAdmin):
    list_display = ["name", "url", "enabled"]
    list_filter = ["enabled"]


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ["heading", "source", "newsletter", "included", "discovered_date"]
    list_filter = ["source", "included"]
    search_fields = ["heading", "summary"]


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ["title", "subject", "status", "created_date", "sent_date"]
    list_filter = ["status"]
    search_fields = ["subject"]
    inlines = [ArticleInline, NewsletterContactInline]


@admin.register(NewsletterContact)
class NewsletterContactAdmin(admin.ModelAdmin):
    list_display = ["newsletter", "contact", "sent_date", "opened_date", "bounced"]
    list_filter = ["bounced"]
