from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.conf import settings
from django.http import HttpResponse
from django.contrib.sites.models import Site
try:
    from django.contrib.auth import get_user_model
    user_model = get_user_model
except ImportError:
    from django.contrib.auth.models import User
    user_model = User
from django.contrib.auth.models import User
from userprofile.models import UserProfile
from feeds.models import Feeds
from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect
from django.template.loader import get_template, render_to_string
from django.template import Template, Context, RequestContext
from friendship.exceptions import AlreadyExistsError
from friendship.models import Friend, Follow, FriendshipRequest

get_friendship_context_object_name = lambda: getattr(settings, 'FRIENDSHIP_CONTEXT_OBJECT_NAME', 'user')
get_friendship_context_object_list_name = lambda: getattr(settings, 'FRIENDSHIP_CONTEXT_OBJECT_LIST_NAME', 'users')

def friend_invite(request):
     if 'email' in request.GET:
         query = request.GET['email']
         if query is not None:
             results = User.objects.get(email=query)
             if results is None:
                 from django.core import send_mail
                 send_mail()
         else:
             query = ""
             results = None

def add_counselor(request):         
    """ Send a invitation to counselor by email """
    user = User.objects.get(email=request.user)
    check = user.profile.counselor_email
    if check is not None:
        try:
            counselor = User.objects.get(email=check)
            return redirect('/friends/follower_add/', username=counselor) 
        except User.DoesNotExist as e:
            from django.core.mail import send_mail
            current_site = Site.objects.get_current()

            subject = render_to_string('friendship/add_counselor_subject.txt',{'site': current_site})
            subject = ''.join(subject.splitlines())
            message = render_to_string('friendship/add_counselor.txt')
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [check])

def view_friends(request, username, template_name='friendship/friend/user_list.html'):
    """ View the friends of a user """
    user = get_object_or_404(user_model, email=username)
    friends = Friend.objects.friends(user)
    return render(request, template_name, {get_friendship_context_object_name():user,'friends': friends})

@csrf_protect
@login_required
def friendship_add_friend(request, to_username, template_name='friendship/friend/add.html'):
    """ Create a FriendshipRequest """
    context = RequestContext(request)

    if request.method == 'POST':
        to_user = user_model.objects.get(email=to_username)
        from_user = request.user
        try:
            Friend.objects.add_friend(from_user, to_user)
        except AlreadyExistsError as e:
            ctx['errors'] = ["%s" % e]
    else:
        return HttpResponseRedirect("/friends/friend/requests/")

    return render(request, template_name, context)

@csrf_protect
@login_required
def friendship_accept(request, friendship_request_id):
    """ Accept a friendship request """
    if request.method == 'POST':
        f_request = get_object_or_404(FriendshipRequest, id=friendship_request_id)
        f_request.accept()
        return redirect('friendship_view_friends', username=request.user.email)

    return redirect('friendship_requests_detail', friendship_request_id=friendship_request_id)


@login_required
def friendship_reject(request, friendship_request_id):
    """ Reject a friendship request """
    if request.method == 'POST':
        f_request = get_object_or_404(FriendshipRequest, id=friendship_request_id)
        f_request.reject()
        return redirect('friendship_request_list')

    return redirect('friendship_requests_detail', friendship_request_id=friendship_request_id)


@login_required
def friendship_cancel(request, friendship_request_id):
    """ Cancel a previously created friendship_request_id """
    if request.method == 'POST':
        f_request = get_object_or_404(FriendshipRequest, id=friendship_request_id)
        f_request.cancel()
        return redirect('friendship_request_list')

    return redirect('friendship_requests_detail', friendship_request_id=friendship_request_id)


@login_required
def friendship_request_list(request, template_name='friendship/friend/requests_list.html'):
    """ View unread and read friendship requests """
    #friendship_requests = Friend.objects.requests(request.user)
    friendship_requests = FriendshipRequest.objects.filter(rejected__isnull=True)

    return render(request, template_name, {'requests': friendship_requests})


@login_required
def friendship_request_list_rejected(request, template_name='friendship/friend/requests_list.html'):
    """ View rejected friendship requests """
    #friendship_requests = Friend.objects.rejected_requests(request.user)
    friendship_requests = FriendshipRequest.objects.filter(rejected__isnull=True)

    return render(request, template_name, {'requests': friendship_requests})


@login_required
def friendship_requests_detail(request, friendship_request_id, template_name='friendship/friend/request.html'):
    """ View a particular friendship request """
    f_request = get_object_or_404(FriendshipRequest, id=friendship_request_id)

    return render(request, template_name, {'friendship_request': f_request})


def followers(request, username, template_name='friendship/follow/followers_list.html'):
    """ List this user's followers """
    user = get_object_or_404(user_model, username=username)
    followers = Follow.objects.followers(user)

    return render(request, template_name, {get_friendship_context_object_name(): user, 'followers': followers})


def following(request, username, template_name='friendship/follow/following_list.html'):
    """ List who this user follows """
    user = get_object_or_404(user_model, username=username)
    following = Follow.objects.following(user)

    return render(request, template_name, {get_friendship_context_object_name(): user, 'following': following})


@login_required
def follower_add(request, femail, template_name='friendship/follow/add.html'):
    """ Create a following relationship """
    ctx = {'femail': femail}

    if request.method == 'POST':
        followee = User.objects.get(email=femail)
        follower = request.user
        try:
            Follow.objects.add_follower(follower, followee)
        except AlreadyExistsError as e:
            ctx['errors'] = ["%s" % e]
        else:
            return redirect('friendship_following', email=follower.email)

    return render(request, template_name, ctx)


@login_required
def follower_remove(request, followee_username, template_name='friendship/remove.html'):
    """ Remove a following relationship """
    if request.method == 'POST':
        followee = user_model.objects.get(username=followee_username)
        follower = request.user
        Follow.objects.remove_follower(follower, followee)
        return redirect('friendship_following', username=follower.username)

    return render(request, template_name, {'followee_username': followee_username})

def sortby_users(request, template_name="friendship/friend/sort.html"):
    if request.user.category == 'C':
        finds = User.objects.filter(category=request.user.category)
    else:
        school = request.user.profile.school_name
        finds = UserProfile.objects.filter(school_name=school)
        for find in finds:
            user = User.objects.get(email=find)
    t = get_template('friendship/friend/sort.html')
    c = Context({'finds':finds})
    return render(request, template_name, {get_friendship_context_object_list_name(): finds})


def all_users(request, template_name="friendship/user_actions.html"):
    users = user_model.objects.all()

    return render(request, template_name, {get_friendship_context_object_list_name(): users})
