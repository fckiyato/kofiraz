from django.shortcuts import render
from django.views import View
#-------------------------------------
class BlogsView(View):
    def get(self, request):
        return render(request, 'blogs/blogs.html')
#-------------------------------------
class BlogsDetailView(View):
    def get(self, request):
        return render(request, 'blogs/blogsdetail.html')
#-------------------------------------