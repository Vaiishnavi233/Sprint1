#from django.http import HttpResponseRedirect
#from django.shortcuts import redirect
#from instamojo_wrapper import Instamojo

#from farmerapp.models import Booking

##api = Instamojo(api_key="test_1bc15839a9776d7ec22a192d55c", auth_token="test_41c435fac3f8400c8aa675da674", endpoint='https://test.instamojo.com/api/1.1/');
 #settings.SITE_DOMAIN + "/payment_status/?book_id=" + str(request.GET.get('book_id'))
# https://e0f737b7b539.ngrok.io/payment_status/?book_id=" + str(request.GET.get('book_id'))
# Create a new Payment Request
# response = api.payment_request_create(
#         amount='100',
#         purpose='Ecommerce Grocery Shop',
#         send_email=True,
#         email="bhuwanbhaskar761@gmail.com",
#         redirect_url= "https://linkedin.com/in/bhuwanbhaskar761"
#         )
# print(response['payment_request']['id'])
#def original_payment(request):
   # print(request.GET.get('total'),"AAAAAAAAAAAAAAA")
    #book = Booking.objects.get(id=request.GET.get('book_id'))
    #response = api.payment_request_create(
     #   amount=request.GET.get('total'),
     #   purpose='Ecommerce Grocery Shop',
      #  send_email=True,
       # email="bhuwanbhaskar761@gmail.com",
        #redirect_url="https://e0f737b7b539.ngrok.io/payment_status/?book_id=" + str(request.GET.get('book_id')),
        #)
    # print the long URL of the payment request.

    #print(response)
    #payment_id = response['payment_request']['id']
    #book.payment_id = payment_id
    #book.save()
    #return HttpResponseRedirect(response['payment_request']['longurl'])

#def payment_status(request):
   # book = Booking.objects.get(id=request.GET.get('book_id'))
    #response = api.payment_request_status(book.payment_id)
    #status = response['payment_request']['status']
    #book.payment_status = status
    #print(status)
    #return redirect('view_booking')-->

from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from instamojo_wrapper import Instamojo
from farmerapp.models import Booking

# Live endpoint
api = Instamojo(
    api_key="your_live_api_key", 
    auth_token="your_live_auth_token", 
    endpoint="https://www.instamojo.com/api/1.1/"
)

def original_payment(request):
    book = Booking.objects.get(id=request.GET.get('book_id'))
    try:
        response = api.payment_request_create(
            amount=request.GET.get('total'),
            purpose='E-Farming Purchase',
            send_email=True,
            email=book.user.email,  # use actual user's email
            redirect_url="https://yourdomain.com/payment_status/?book_id=" + str(book.id),
        )

        if response['success']:
            payment_id = response['payment_request']['id']
            book.payment_id = payment_id
            book.save()
            return HttpResponseRedirect(response['payment_request']['longurl'])
        else:
            print("Payment creation failed:", response)
            return redirect('payment_failed')

    except Exception as e:
        print("Instamojo error:", e)
        return redirect('payment_failed')

def payment_status(request):
    book = Booking.objects.get(id=request.GET.get('book_id'))
    try:
        response = api.payment_request_status(book.payment_id)
        status = response['payment_request']['status']
        book.payment_status = status
        book.save()
        return redirect('view_booking')
    except Exception as e:
        print("Status fetch error:", e)
        return redirect('payment_failed')
