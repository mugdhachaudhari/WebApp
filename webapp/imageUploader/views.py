from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseForbidden
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.context_processors import csrf
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.csrf import csrf_protect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages

from imageUploader.forms import *
from imageUploader.models import *

# Create your views here.
@ensure_csrf_cookie
def uploadImage(request):
    message = '';
    request.session['userid'] = request.user.id
    # if (User.objects.filter(id = request.session['userid']).exists()):
    #     return HttpResponse(request.session['userid'])

    # If image upload form submitted then image would be saved
    if request.method == 'POST':
        # Form is created with request information and checked whether form is valid
        form = imageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # if form is valid then image model instance is created and its attributes are initialized with user input.
            newImage = imageModel()
            # return HttpResponse(request.FILES['image'])
            newImage.modelPic = request.FILES['image']
            newImage.caption = request.POST['caption']
            # If user is logged in, then user id attribute would be initialized with session user id
            if (request.user).username:
                newImage.user_id = request.user.id;
            #     Image would be saved in sqlite3 database.
            newImage.save()
            message = 'Image uploaded successfully'
    else:
        # If request is not POST, then blank image upload form would be generated
        form = imageUploadForm()

    # If user is not logged in, then all images would be selected otherwise only images uploaded by user would be selected
    if not(request.user.username):
        images = imageModel.objects.all();
    else:    
        images = imageModel.objects.filter(user_id = request.user.id);

    # Paginator instance created for 10 pages per page. If error in retrieving page then depending on error first or last page would be returned
    paginator = Paginator(images, 10)
    page = request.GET.get('page')
    try:
        imagePage = paginator.page(page)
    except PageNotAnInteger:
        imagePage = paginator.page(1)
    except EmptyPage:
        imagePage = paginator.page(paginator.num_pages)

    # Data would be passed to imageUpload.html
    return render_to_response('imageUpload.html', {'imagePage' : imagePage, 'form' : form, 'message' : message}, context_instance=RequestContext(request))


@ensure_csrf_cookie
def deleteImage(request):
    # Image would be deleted.
    if request.user.username and imageModel.objects.filter(id = request.GET.get('id'), user_id = request.session['userid']).exists():
        imageModel.objects.filter(id = request.GET.get('id')).delete()
        message = 'Image deleted successfully'

        return render_to_response('imageDelete.html', {'message' : message}, context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/')

@ensure_csrf_cookie
def editImage(request):
    if request.user.username:
        message = '';
        if request.method == 'POST':
            # If request method is POST then form would be created with info.
            form = imageEditForm(request.POST, request.FILES)
            if form.is_valid():
                image = imageModel.objects.get(id = request.POST['imageId'])
                image.caption = request.POST['caption']
                image.save()
                message = 'Image caption updated successfully'
                image = imageModel.objects.get(id = request.POST['imageId'])
        else:
            # If request method not POST then form would be initialized with stored caption for that image.
            if imageModel.objects.filter(id = request.GET.get('id'), user_id = request.session['userid']).exists():
                image = imageModel.objects.get(id = request.GET.get('id'))
                form = imageEditForm(initial = { 'caption' : image.caption })
            else:
                return HttpResponseRedirect('/')

        return render_to_response('imageEdit.html', {'image' : image, 'form' : form, 'message' : message}, context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect("/")

@csrf_protect
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        # Form fileds would be validated before addign data in table.
        if form.is_valid():
            user = User.objects.create_user(
                first_name=form.cleaned_data['firstname'],
                last_name=form.cleaned_data['lastname'],
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
                email=form.cleaned_data['email']
            )
            request.session['email'] = form.cleaned_data['email']       
            return HttpResponseRedirect('/register/success/')
    else:
        form = RegistrationForm()
    variables = RequestContext(request, {'form': form})
    # Data is given to registration/register.html
    return render_to_response('registration/register.html',variables,)

def register_success(request):
    return render_to_response('registration/success.html',)
