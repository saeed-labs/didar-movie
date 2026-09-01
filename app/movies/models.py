from django.db import models
from categories.models import ActorsModel, DirectorModel, GenreModel


class MoviesModel(models.Model):
    title = models.CharField(max_length=100, unique=True, db_index=True, verbose_name='عنوان فیلم')
    slug = models.SlugField(unique=True, db_index=True, verbose_name='اسلاگ')
    image = models.ImageField(upload_to='movies/%Y/%m', verbose_name='تصویر')
    description = models.TextField(verbose_name='توضیحات')
    short_description = models.TextField(verbose_name='توضیحات کوتاه')
    genres = models.ManyToManyField(GenreModel, related_name='genres', verbose_name='ژانرها')
    actors = models.ManyToManyField(ActorsModel, related_name='actors', verbose_name=' بازیگران')
    directors = models.ManyToManyField(DirectorModel, related_name='directors', verbose_name='کارگردان')
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    is_featured = models.BooleanField(default=False, verbose_name='ویژه')
    release_date = models.DateField(verbose_name='تاریخ انتشار')
    price = models.PositiveBigIntegerField(default=0,verbose_name='قیمت خرید', help_text='براساس تومان')
    # discount = models.PositiveSmallIntegerField(default=0, verbose_name='تخفیف')
    most_viewed = models.PositiveIntegerField(default=0, verbose_name='پربازدید', db_index=True)
    beloved = models.PositiveIntegerField(default=0, verbose_name='محبوب', db_index=True)
    is_double = models.BooleanField(default=False, verbose_name='دوبله')



    created_on = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_on = models.DateTimeField(auto_now=True, verbose_name='تاریخ به‌روزرسانی')
    #
    # @property
    # def final_price(self):
    #     if self.discount > 0:
    #         return self.price - (self.price * self.discount // 100)
    #
    #     return self.price



    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_on']
        verbose_name = 'فیلم و سریال'
        verbose_name_plural = 'فیلم و سریال ها'







class MovieVideoModel(models.Model):
    movie = models.ForeignKey(MoviesModel, on_delete=models.CASCADE, related_name='movie_videos')
    file = models.FileField(upload_to='movies/%Y/%m')
    is_trailer = models.BooleanField(default=False, )
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'ویدیوی فیلم'
        verbose_name_plural = 'ویدیوهای فیلم'
        ordering = ['-created_on']

    def __str__(self):
        return self.movie.title