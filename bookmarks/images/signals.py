from django.db.models.signals import m2m_changed #la señal con la que se va a trabajar, indica cuando se va a cambiar una relacion muchos a muchos
from django.dispatch import receiver # me permite decorar una funcion y que reciba y responda a la seña m2m_changed
from .models import Image 


@receiver(m2m_changed, sender=Image.users_like.through) 
def users_like_changed(sender, instance, **kwargs):
    instance.total_likes = instance.users_like.count() #cuantos usuarios de han dado like
    instance.save() #se guarda y ejectuta 
    
