from django.db import models

#--------- Tblevento ----------#
class TbleventoQuerySet(models.QuerySet):
    def activos(self):
        return self.filter(cceevento = 'A')

class TbleventoManager(models.Manager):
    def get_queryset(self):
        return TbleventoQuerySet(self.model, using=self._db) #Important

    def activos(self):
        return self.get_queryset().activos()
