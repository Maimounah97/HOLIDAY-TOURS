from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import *
import bcrypt

def home(request):
    return render(request, 'login.html')

def handle_registration(request):
    if request.method == "POST":
        errors = User.objects.basic_validation(request.POST)
        if len(errors) > 0:
            for key, errorMessage in errors.items():
                messages.error(request, errorMessage)
            return redirect('home')
        else:
            first_name = request.POST["first_name"]
            last_name = request.POST["last_name"]
            email = request.POST["email"]
            password = request.POST['password']
            
            hash_n_salt = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            newuser = User.objects.create(first_name=first_name,last_name=last_name,email=email, password = hash_n_salt)
            newuser.save()
            request.session['userid'] = newuser.id
            messages.success(request, "User has been created")
            return redirect('home')
    return render(request, 'register.html')
def handle_login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        try:
            user = User.objects.get(email=email)
            if bcrypt.checkpw(password.encode(), user.password.encode()):
                request.session['userid'] = user.id
                
                return redirect('all_trips')
            else:
                messages.error(request, "User password do not match")
        except User.DoesNotExist:
            messages.error(request, "User not found")
    
    return redirect('home')

def logout(request):
    request.session.clear()
    messages.success(request, "You have been logged out!")
    return redirect('home')

def all_tripss(request):
    if "userid" not in request.session:
        return render(request,"authenticate.html")
    current_user=User.objects.get(id=request.session['userid'])
    trips_added_by_currentUser = Trip.objects.filter(created_user=current_user)
    all_tripss=Trip.objects.exclude(created_user=current_user)
    likedTrips=current_user.added_trips.all()
    context={
        'current_user':current_user,
        'all_trips':all_tripss,
        'trips_added_by_currentUser':trips_added_by_currentUser,
        'likedTrips':likedTrips,
    }
    return render(request, 'all_trips.html', context)

def add_trip(request):
    if "userid" not in request.session:
        return render(request,"authenticate.html")
    current_user=User.objects.get(id=request.session['userid'])
    if request.method == "POST":
            errors = Trip.objects.validator(request.POST, request.FILES)
            print(errors)
            if (len(errors ) > 0):
                for key, value in errors.items():
                    messages.error(request, value)
                return redirect( "/addtrip")
            else:
                
                name=request.POST['name']
                description=request.POST['description']
                start_date=request.POST['start_date']
                end_date=request.POST['end_date']
                image=request.FILES.get('image')
                # if len(request.FILES['image'])!=0:    
                #     image=request.FILES.get('image')      
                # else:
                #     messages.error(request, "Sorry, image filed cannot be empty")
                newTrip=Trip.objects.create(name=name, description=description, start_date=start_date, end_date=end_date, created_user=current_user, image=image)
                newTrip.save()
                
                return redirect('all_trips')
    
    return render(request, 'add_trip.html')

def addToLikedTrip(request, tripId):
    if "userid" not in request.session:
        return render(request,"authenticate.html")
    current_user=User.objects.get(id=request.session['userid'])
    liked_trip=Trip.objects.get(id=tripId)
    current_user.added_trips.add(liked_trip)
    return redirect('/likedTrips')

def likedTrips(request):
    if "userid" not in request.session:
        return HttpResponse("Please authenticate first")
    current_user=User.objects.get(id=request.session['userid'])
    likedTrips=current_user.added_trips.all()
    context={
        'current_user':current_user,
        'likedTrips':likedTrips,
    }
    return render(request,'likedTrips.html', context)

def deleteTrip(request, tripId):
    if "userid" not in request.session:
        return render(request,"authenticate.html")
    trip_to_delete = Trip.objects.get(id=tripId)	
    trip_to_delete.delete()
    return redirect('all_trips') 

def removeTrip(request, tripId):
    if "userid" not in request.session:
       return render(request,"authenticate.html")
    trip_to_remove = Trip.objects.get(id=tripId)
    current_user = User.objects.get(id=request.session["userid"])
    trip_to_remove.users.remove(current_user)
    return redirect('/likedTrips')

def view_trip(request , tripId):
    if "userid" not in request.session:
        return render(request,"authenticate.html")
    trip = Trip.objects.get(id=tripId)
    users=trip.users.all()
    context = {   
        "trip": trip,
        "users": users,    
    }
    return render(request, "view-trip.html", context)

def trip_reviews(request,tripId):
    # trip=Trip.objects.get(id=tripId)
    # context={
    #     'reviews': trip.reviews.all().order_by("-created_at"),
    #      }
    return redirect(f"/postreview?id={tripId}")
    # return render(request, 'view_review.html', context)

# def review_comments(request,reviewId):
#     pass

def post_review(request):
    if "userid" not in request.session:
        return render(request,"authenticate.html")
    tripId=request.GET['id']
    current_user=User.objects.get(id=request.session['userid'])
    if request.method=='POST':
        rev=request.POST['rev']
        
        trip=Trip.objects.get(id=tripId)
        newReview=Review.objects.create(riv=rev, user=current_user ,trip=trip)
        newReview.save()
        return redirect('trip_reviews', trip.id)
    trip=Trip.objects.get(id=tripId)
    context={
        'reviews': trip.reviews.all().order_by("-created_at"),
        'current_user':current_user,
        'trip':Trip.objects.get(id=tripId)
         }
    return render(request, 'view_review.html', context)
def post_comment(request,reviewId):
    if "userid" not in request.session:
        return render(request,"authenticate.html")
    trip_object=Review.objects.get(id=reviewId)
    tripId=trip_object.trip.id
    current_user=User.objects.get(id=request.session['userid'])
    if request.method=='POST':
        comment=request.POST['comment']
        
        current_review=Review.objects.get(id=reviewId)
        # current_trip=current_review.trip.objects()
        newComment=Comment.objects.create(comment=comment, poster=current_user, on_reviews=current_review)
        newComment.save()
      
    return redirect(f'/reviews/{tripId}') 

def delete_review(request,reviewId):
    if "userid" not in request.session:
        return render(request,"authenticate.html")
    review_to_delete = Review.objects.get(id=reviewId)	
    tripId=review_to_delete.trip.id
    review_to_delete.delete()
    return redirect(f'/reviews/{tripId}')

def delete_comment(request,commentId):
    if "userid" not in request.session:
        return render(request,"authenticate.html")
    comment_to_delete = Comment.objects.get(id=commentId)	
    review_obj=comment_to_delete.on_reviews
    tripId=review_obj.trip.id
    comment_to_delete.delete()
    return redirect(f'/reviews/{tripId}') 


