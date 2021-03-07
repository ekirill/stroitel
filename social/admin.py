from django.contrib import admin
from django import forms

from social.models import Comment


class CommentForm(forms.ModelForm):
    message = forms.CharField(widget=forms.Textarea(attrs={'rows': 10, 'cols': 100}), label="Комментарий")

    class Meta:
        model = Comment
        fields = ('entry', 'author', 'published_at', 'is_visible', 'message')


class CommentAdmin(admin.ModelAdmin):
    form = CommentForm
    ordering = ('-published_at', )
    list_display = ('published_at', 'entry', 'author')
    readonly_fields = ('published_at', 'entry', 'author')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.select_related('entry', 'author')
        return qs


admin.site.register(Comment, CommentAdmin)
