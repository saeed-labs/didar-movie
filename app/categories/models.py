from django.db import models



class ActorsModel(models.Model):
    name = models.CharField(max_length=100, verbose_name='نام')
    image = models.ImageField(upload_to='images/', verbose_name='عکس')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='اسلاگ')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'بازیگر'
        verbose_name_plural = "بازیگران"




class DirectorModel(models.Model):
    name = models.CharField(max_length=100, verbose_name='نام')
    image = models.ImageField(upload_to='images/', verbose_name='عکس')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='اسلاگ')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)



    def __str__(self):
        return self.name
    class Meta:
        verbose_name = 'کارگردان'
        verbose_name_plural = 'کارگردانان'


class GenreModel(models.Model):
    name = models.CharField(max_length=100, verbose_name='نام ژانر')
    parent = models.ForeignKey("self", on_delete=models.PROTECT, null=True, blank=True, related_name="children", verbose_name='زیر دسته')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='اسلاگ')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'ژانر'
        verbose_name_plural = 'ژانرها'