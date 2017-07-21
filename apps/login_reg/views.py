# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse, reverse, redirect
from django.contrib import messages
from models import *

#DONE
def index(request):
    if 'current_id' in request.session and request.session['current_id'] !=0 :
        return redirect(reverse("quote_home"))
    return render(request, 'login_reg/index.html')

#DONE
def authenticate(request):
    if request.method !='POST':
        return redirect('/main')

    new_user=False

    if request.POST['auth_type']=='register':
        new_user = True
        errors=User.objects.register_validator(request.POST)
    else:
        errors=User.objects.login_validator(request.POST)

    if len(errors):
        for error,error_message in errors.iteritems():
            messages.error(request, error_message)
        return redirect('/main')

    email = request.POST['email']
    password = request.POST['password']
    if new_user:
        first_name = request.POST['first_name']
        print first_name
        last_name = request.POST['last_name']
        print last_name
        alias = request.POST['alias']
        print alias
        confirm = request.POST['confirm']
        print confirm
        birthday = request.POST['birthday']
        print birthday
        hashed_key=bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        print hashed_key
        newUser=User.objects.create(first_name = first_name, last_name = last_name, email = email, alias=alias, password=hashed_key,birthday=birthday)
        request.session['current_id']=newUser.id
        request.session['current_first_name'] = first_name
        request.session['current_last_name'] = last_name
                    
    else:
        this_user=User.objects.get(email=email)
        request.session['current_first_name'] = this_user.first_name
        print request.session['current_first_name']
        request.session['current_last_name'] = this_user.last_name
        print request.session['current_last_name']
        request.session['current_id'] = this_user.id
        print request.session['current_id']
        
    request.session['current_email'] = email
        
    return redirect("/quotes")


#DONE
def logout(request):
    request.session['current_first_name'] = ''
    request.session['current_last_name'] = ''
    request.session['current_email'] = ''
    request.session['current_id'] = 0
    return redirect('/main')

def quote_home(request):
    if not request.session['current_id']:
        return redirect('/main')
    current_user=request.session['current_id']
    print current_user
    not_favorited=Quote.objects.all().exclude(favorited__id=current_user)
    for quote in not_favorited:
        print quote.attributed_to, quote.quote, quote.created_by.first_name
    favorited=Quote.objects.filter(favorited__id=current_user)
    print "these are favorited"
    for quote in favorited:
        print quote.attributed_to, quote.quote, quote.created_by.first_name
    
    
    context= {
        "first" : request.session['current_first_name'],
        "id" : request.session['current_id'],
        "not_favorited" : not_favorited,
        "favorited" : favorited,
    }
    return render(request, "login_reg/quotes_home.html", context)


def user_info(request,user_id):
    if not request.session['current_id']:
        return redirect('/main')
    added_quotes = Quote.objects.filter(created_by__id = user_id)    
    print len(added_quotes)
    
    context= {
        "first" : request.session['current_first_name'],
        "id" : request.session['current_id'],
        "quotes" : added_quotes,
        "quote_count": len(added_quotes)
    }
    return render(request, "login_reg/user_info.html", context)

#DONE
def quote_add(request):
    if not request.session['current_id']:
        return redirect('/main')
    if request.method!='POST':
        return redirect('/quotes')
    errors = False
    attributed_to=request.POST['attributed_to']
    print attributed_to
    if len(attributed_to) < 3:
        messages.error(request,'Quoted_by needs to be at least 3 chars')
        errors = True
    quote=request.POST['quote']
    if len(quote) < 10:
        messages.error(request, 'Quote needs to be at least 10 chars')
        errors = True
    user_id=request.POST['user_id']
    print user_id
    print quote
    if not errors:
        curr_user = User.objects.get(id = user_id )
        x = Quote.objects.create(quote=quote, attributed_to=attributed_to,created_by = curr_user)
        print x
    return redirect("/quotes")


def favorite_delete(request,quote_id):
    if not request.session['current_id']:
        return redirect('/main')
    current_quote = Quote.objects.get(id = quote_id)
    current_quote.save()
    print current_quote
    current_user = User.objects.get(id = request.session['current_id'])
    current_user.save()
    print current_user
    current_quote.favorited.remove(current_user)
    return redirect(reverse("quote_home"))

def favorite_add(request,quote_id):
    if not request.session['current_id']:
        return redirect('/main')
    current_quote = Quote.objects.get(id = quote_id)
    current_quote.save()
    print current_quote
    current_user = User.objects.get(id = request.session['current_id'])
    current_user.save()
    print current_user
    current_quote.favorited.add(current_user)
    return redirect(reverse("quote_home"))
