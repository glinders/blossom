from django.shortcuts import render


posts = [
    {
        'author': 'Geert',
        'title': 'blog 1',
        'content': 'content blog 1',
        'date_posted': '1 July, 2024',
    },
    {
        'author': 'Brenda',
        'title': 'blog 2',
        'content': 'content blog 2',
        'date_posted': '1 May, 2024',
    },
]


def home(request):
    context = {
        'posts': posts,
    }
    return render(request, 'ccf/home.html', context)


def about(request):
    return render(request, 'ccf/about.html', {'title': 'About'})
