from django import forms
from .models import Post, Category, Comment


class PostForm(forms.ModelForm):
    # Let admin create categories inline via a text field
    new_category = forms.CharField(
        max_length=60, required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Or type a new category name…',
            'id': 'id_new_category',
        }),
        label='New category (optional)',
    )

    class Meta:
        model = Post
        fields = ['title', 'category', 'cover_color', 'excerpt', 'body', 'status']
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': ' ',
                'id': 'id_title',
            }),
            'cover_color': forms.TextInput(attrs={
                'type': 'color',
                'id': 'id_cover_color',
                'style': 'width:60px;height:36px;padding:2px;border-radius:6px;cursor:pointer;',
            }),
            'excerpt': forms.Textarea(attrs={
                'placeholder': ' ',
                'rows': 2,
                'id': 'id_excerpt',
            }),
            'body': forms.Textarea(attrs={
                'placeholder': ' ',
                'rows': 14,
                'id': 'id_body',
                'class': 'blog-body-input',
            }),
            'status': forms.Select(attrs={'id': 'id_status'}),
            'category': forms.Select(attrs={'id': 'id_category'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].required = False
        self.fields['category'].empty_label = '— No category —'
        self.fields['excerpt'].required = False

    def save(self, commit=True):
        post = super().save(commit=False)
        # Handle inline category creation
        new_cat_name = self.cleaned_data.get('new_category', '').strip()
        if new_cat_name:
            cat, _ = Category.objects.get_or_create(name=new_cat_name)
            post.category = cat
        if commit:
            post.save()
        return post


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={
                'placeholder': 'Write a comment…',
                'rows': 3,
                'id': 'id_comment_body',
            }),
        }
        labels = {'body': ''}
