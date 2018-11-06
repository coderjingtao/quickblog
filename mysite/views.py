from django.shortcuts import render

# public pages
def aboutme(request):
    return render(request,'about_me.html')