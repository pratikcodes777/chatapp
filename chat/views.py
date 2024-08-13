from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from .models import Room, Message
# Create your views here.

def home(request):
    return render(request, 'home.html')

def room(request , room):
    username = request.GET.get('username')
    room_details = Room.objects.get(name=room)
    context ={
        'username': username,
        'room': room,
        'room_details': room_details
    }
    return render(request , 'room.html', context)

def checkview(request):
    room = request.POST['room_name']
    username = request.POST['username']

    if Room.objects.filter(name=room).exists():
        return redirect(f'/{room}/?username={username}')
    else:
        new_room =Room.objects.create(name=room)
        new_room.save()
        return redirect(f'/{room}/?username={username}')



def send(request):
    username = request.POST.get('username')
    room_id = request.POST.get('room_id')
    message = request.POST.get('message')

    room = Room.objects.get(id=room_id)
    new_message = Message.objects.create(value=message, room=room, user=username)
    new_message.save()

    return HttpResponse('Message sent successfully')



def getMessages(request, room):
    room_details = Room.objects.get(name = room)

    messages = Message.objects.filter(room = room_details.id)
    return JsonResponse({'messages': list(messages.values())})


def delete_message(request, message_id):
    if request.method == 'DELETE':
        try:
            message = Message.objects.get(id=message_id)
            message.delete()
            return JsonResponse({'success': True})
        except Message.DoesNotExist:
            return JsonResponse({'error': 'Message not found'}, status=404)
    return JsonResponse({'error': 'Invalid request'}, status=400)

