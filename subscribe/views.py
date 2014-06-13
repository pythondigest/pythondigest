from django.contrib import messages
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import FormView, DeleteView

from .models import Subscribers
from .forms import AddSubscriber


class AddSubscriber(FormView):
    template_name = "add_subscriber.html"
    form_class = AddSubscriber

    def get_success_url(self):
        email = self.request.POST['useremail']
        Subscribers.objects.create(useremail=email)
        messages.info(
            self.request, u'Ваш адрес добавлен в список рассылки'
            )
        return '/'


#class DeleteSubscriber(DeleteView):
#    model = Subscribers
#    success_url = reverse_lazy('useremail')



def unsubscribe(request, username, token):

    user = get_object_or_404(Subscribers, id_subscriber=token)
    tmp = user.useremail.split('@')[0]
    if username == tmp:
        user.subscribe = False
        user.delete()
        messages.info(
        request, u'Ваш адрес удален из списка рассылки'
        )
        return redirect('/')
    return Http404
