from django.contrib import admin
from django import forms

from social.models import Comment, Voting, VotingVariant


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


class VotingVariantInlineFormSet(forms.BaseInlineFormSet):
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.select_related('author')


class VotingVariantInline(admin.TabularInline):
    ordering = ('order', '-published_at', )
    fields = ('variant', 'order', 'author_name')
    readonly_fields = ('author_name',)
    formset = VotingVariantInlineFormSet
    model = VotingVariant
    extra = 1


class VotingAdmin(admin.ModelAdmin):
    inlines = [VotingVariantInline]
    list_display = ("question", "order")
    list_editable = ("order",)


admin.site.register(Comment, CommentAdmin)
admin.site.register(Voting, VotingAdmin)
