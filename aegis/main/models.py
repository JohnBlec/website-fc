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


class Members(models.Model):
    name = models.CharField('Название', max_length=50)
    logo = models.ImageField('Эмблема', upload_to='main/img/MembersAE', default='main/img/MembersAE/NoLogo.png')
    q_we = models.BooleanField('Наша ли команда?', default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Участник'
        verbose_name_plural = 'Участники'


class Matches(models.Model):
    date = models.DateField('Дата проведения матча')
    stage = models.CharField('Стадия', max_length=30)
    table = models.ForeignKey('Tables', on_delete=models.CASCADE, null=True,)
    home_team = models.ForeignKey('Members', on_delete=models.SET_NULL, null=True,
                                  verbose_name="Домашняя команда", related_name='home_team')
    away_team = models.ForeignKey('Members', on_delete=models.SET_NULL, null=True,
                                  verbose_name="Гостевая команда", related_name='away_team')
    home_goals = models.DecimalField('Голы домашней комадны', max_digits=3, decimal_places=0, null=True)
    away_goals = models.DecimalField('Голы домашней комадны', max_digits=3, decimal_places=0, null=True)

    def __str__(self):
        return self.stage

    class Meta:
        verbose_name = 'Участник'
        verbose_name_plural = 'Участники'


class Tables(models.Model):
    start_date = models.DateField('Начало турнира')
    end_date = models.DateField('Окончание турнира', null=True)
    tournament = models.ForeignKey('Tournaments', on_delete=models.SET_NULL, null=True, verbose_name="Турнир")
    update_date = models.DateField('Обновление данных таблицы', null=True)
