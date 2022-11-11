from django.db import models


class Players(models.Model):
    name = models.CharField('Фамилия', max_length=30)
    number = models.PositiveSmallIntegerField('Игровой номер')
    photo = models.ImageField('Фото', upload_to='main/img/PlayersAE')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Игрок'
        verbose_name_plural = 'Игроки'

class Tournaments(models.Model):
    name = models.CharField('Название', max_length=50)
    photo = models.ImageField('Логотип', upload_to='main/img/TournamentAE')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Турнир'
        verbose_name_plural = 'Турниры'

