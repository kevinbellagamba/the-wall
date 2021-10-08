from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from loginApp.models import User
from wallApp.models import MessagePost, Comment

# Create your views here.
def wallIndex(request):
    if 'user' not in request.session:
        return redirect('/')
    context = {
        'all_messages': MessagePost.objects.all(),
        'user' : User.objects.get(id=request.session['user']),
        'posts' : MessagePost.objects.all(),
        'comments' : Comment.objects.all(),
    }
    return render(request, 'wall.html', context)

def createPost(request):
    if request.method == 'POST':
        LoggedUser = User.objects.get(id=request.session['user'])
        MessagePost.objects.create(
            content = request.POST['content'],
            poster=LoggedUser
        )

        return redirect('/wall')

def createComment(request):
    if request.method == 'POST':
        LoggedUser = User.objects.get(id=request.session['user'])
        Comment.objects.create(
            content=request.POST['content'],
            poster=LoggedUser,
            message=MessagePost.objects.get(id=request.POST['message']),
    )

        return redirect('/wall')

def deleteMessage(request, message_id):
    delete = MessagePost.objects.get(id=message_id)
    delete.delete()
    return redirect('/wall')
