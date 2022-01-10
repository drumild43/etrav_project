from django import http
from django.db.models import Avg
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Booking, EtravUser, Hotel, Review

def home(request, user_id=None):
    if user_id:
        curr_user = EtravUser.objects.get(pk=user_id)
        context = {'curr_user': curr_user}
    else:
        context = {}
    return render(request, 'core/homepage.html', context=context)

def signup(request, hotel_id=None):
    if request.method == 'GET':
        return render(request, 'core/signup.html', context={'hotel_id': hotel_id})

    elif request.method == 'POST':
        first_name = request.POST['first_name'].strip()
        last_name = request.POST['last_name'].strip()
        email = request.POST['email'].strip()
        password1 = request.POST['password1'].strip()
        password2 = request.POST['password2'].strip()
        
        # if user already exists, prompt to sign in
        if list(EtravUser.objects.filter(email=email)):
            context = {'already_exists': True, 'hotel_id': hotel_id}
            return render(request, 'core/signup.html', context=context)

        # else, create new user if passwords match
        elif password1 == password2:
            new_user = EtravUser(
                first_name=first_name, 
                last_name=last_name, 
                email=email, 
                logged_in = True
            )
            new_user.set_password(password1)
            new_user.save()

            if hotel_id:
                return HttpResponseRedirect(
                    reverse('core:hotel-details', args=(new_user.id, hotel_id))
                )
            else:
                return HttpResponseRedirect(reverse('core:homepage', args=(new_user.id,)))

        # else prompt that passwords do not match
        else:
            context = {
                'error_message': "Passwords do not match.",
                'hotel_id': hotel_id,
                'first_name': first_name,
                'last_name': last_name,
                'email': email
            }
            return render(request, 'core/signup.html', context=context)


def signin(request, hotel_id=None):
    context={'hotel_id': hotel_id}

    if request.method == 'GET':
        return render(request, 'core/signin.html', context=context)

    elif request.method == 'POST':
        email = request.POST['email'].strip()
        password = request.POST['password'].strip()

        try:
            etravuser = EtravUser.objects.get(email=email)
        except EtravUser.DoesNotExist:
            context['error_message'] = "No account with this email id exists."
            return render(request, 'core/signin.html', context=context)

        # if correct password
        if etravuser.check_password(password):
            etravuser.logged_in = True
            etravuser.save()

            if hotel_id:
                return HttpResponseRedirect(
                    reverse('core:hotel-details', args=(etravuser.id, hotel_id))
                )
            else:
                return HttpResponseRedirect(reverse('core:homepage', args=(etravuser.id,)))
        # incorrect password
        else:
            context['error_message'] = "Incorrect password."
            return render(request, 'core/signin.html', context=context)

def logout(request, user_id):
    if request.method == 'POST':
        curr_user = EtravUser.objects.get(pk=user_id)
        curr_user.logged_in = False
        curr_user.save()

    return HttpResponseRedirect(reverse('core:anon_homepage'))

def account(request, user_id):
    curr_user = EtravUser.objects.get(pk=user_id)
    return render(request, 'core/account.html', context={'curr_user': curr_user})

def pers_details(request, user_id):
    curr_user = EtravUser.objects.get(pk=user_id)

    if request.method == 'GET':
        return render(request, 'core/pers-details.html', context={'curr_user': curr_user})

    if request.method == 'POST':
        curr_password = request.POST['curr_password'].strip()
        new_first_name = request.POST.get('first_name')
        new_last_name = request.POST.get('last_name')
        new_password = request.POST.get('new_password')

        if curr_user.check_password(curr_password):
            if new_first_name:
                curr_user.first_name = new_first_name

            if new_last_name:
                curr_user.last_name = new_last_name

            if new_password:
                curr_user.set_password(new_password)

            curr_user.save()

            return HttpResponseRedirect(reverse('core:account', args=(user_id,)))

        # if current password entered is wrong
        else:
            context = {
                'curr_user': curr_user,
                'new_first_name': new_first_name,
                'new_last_name': new_last_name,
                'error_message': "The current password you have entered is incorrect."
            }
            return render(request, 'core/pers-details.html', context=context)

def cancel_booking(request, user_id, booking_id):
    if request.method == 'POST':
        booking = Booking.objects.get(pk=booking_id)
        booking.status = 'X'
        booking.save()
        
        return HttpResponseRedirect(reverse('core:account', args=(user_id,)))

def hotels(request, user_id=None):
    if request.method == 'GET':
        # filter by city
        city = request.GET.get('city')

        if city:
            hotels = Hotel.objects.filter(city__name=city)
        else:
            hotels = Hotel.objects.all()

        # filter by stars
        one_star = request.GET.get('one-star-filter')
        two_star = request.GET.get('two-star-filter')
        three_star = request.GET.get('three-star-filter')
        four_star = request.GET.get('four-star-filter')
        five_star = request.GET.get('five-star-filter')

        star_filters = [one_star, two_star, three_star, four_star, five_star]

        stars = [i for i in [1,2,3,4,5] if star_filters[i-1]]
        hotels = hotels.filter(stars__in=stars) if stars else hotels

        # sort
        sort_criterion = request.GET.get('sort')

        if sort_criterion == "sort_price_HtoL":
            hotels = hotels.order_by('-standard_room_price')
            
        if sort_criterion == "sort_price_LtoH":
            hotels = hotels.order_by('standard_room_price')

        if sort_criterion == "sort_rating_HtoL":
            hotels = hotels.annotate(avg_rating=Avg('review__rating')).order_by('-avg_rating')

        if sort_criterion == "sort_rating_LtoH":
            hotels = hotels.annotate(avg_rating=Avg('review__rating')).order_by('avg_rating')

        if sort_criterion == "sort_name_AtoZ":
            hotels = hotels.order_by('name')

        if sort_criterion == "sort_name_ZtoA":
            hotels = hotels.order_by('-name')
        
        context = {
            'hotels': hotels, 
            'sort_criterion': sort_criterion,
            'city': city,
            'one-star-filter': one_star,
            'two-star-filter': two_star,
            'three-star-filter': three_star,
            'four-star-filter': four_star,
            'five-star-filter': five_star,
            'checkin-date': request.GET.get('checkin-date'),
            'checkout-date': request.GET.get('checkout-date'),
            'person-count': request.GET.get('person-count')
        }
        if user_id:
            curr_user = EtravUser.objects.get(pk=user_id)
            context['curr_user'] = curr_user

        return render(request, 'core/hotels.html', context=context)

def hotel_details(request, hotel_id, user_id=None):
    if request.method == 'GET':
        hotel = Hotel.objects.get(id = hotel_id)
        context = {'hotel': hotel}

        if user_id:
            curr_user = EtravUser.objects.get(pk=user_id)
            context['curr_user'] = curr_user

        return render(request, 'core/hotel-details.html', context=context)

def review(request, user_id, hotel_id):
    if request.method == 'POST':
        review_text = request.POST['review-text']
        rating = int(request.POST['rating'])

        review_list = list(Review.objects.filter(
            user__pk=user_id,
            hotel__pk=hotel_id
        ))

        # if review already exists
        if review_list:
            review = review_list[0]
            review.review_text = review_text
            review.rating = rating

        # if review does not exist, create new review
        else:
            review = Review(
                hotel=Hotel.objects.get(pk=hotel_id),
                user=EtravUser.objects.get(pk=user_id),
                review_text=review_text,
                rating=rating
            )

        review.save()
        return HttpResponseRedirect(reverse('core:hotel-details', args=(user_id, hotel_id)))