from django.db import models
import locale
locale.setlocale(locale.LC_ALL, "")


class Players(models.Model):
    name = models.CharField('Фамилия', max_length=30)
    number = models.PositiveSmallIntegerField('Игровой номер')
    photo = models.ImageField('Фото', upload_to='main/img/PlayersAE', null=True)
    link_vk = models.CharField('Ссылка на вк', max_length=100, null=True)

    def __str__(self):
        return self.name


class Tournaments(models.Model):
    name = models.CharField('Название', max_length=50)
    photo = models.ImageField('Логотип', upload_to='main/img/TournamentAE')

    def __str__(self):
        return self.name


class Members(models.Model):
    name = models.CharField('Название', max_length=50)
    logo = models.ImageField('Эмблема', upload_to='main/img/MembersAE', default='main/img/MembersAE/NoLogo.png')
    q_we = models.BooleanField('Наша ли команда?', default=False)

    def __str__(self):
        return self.name


class Matches(models.Model):
    date = models.DateField('Дата проведения матча')
    stage = models.CharField('Стадия', max_length=30)
    table = models.ForeignKey('Tables', on_delete=models.CASCADE)
    home_team = models.ForeignKey('Members', on_delete=models.CASCADE,
                                  verbose_name="Домашняя команда", related_name='home_team')
    away_team = models.ForeignKey('Members', on_delete=models.CASCADE,
                                  verbose_name="Гостевая команда", related_name='away_team')
    home_goals = models.DecimalField('Голы домашней комадны', max_digits=3, decimal_places=0, null=True)
    away_goals = models.DecimalField('Голы домашней комадны', max_digits=3, decimal_places=0, null=True)
    link_vk = models.CharField('Ссылка на вк', max_length=100, null=True)

    def __str__(self):
        return self.stage

    def get_m_y(self):
        return self.date.strftime('%B %Y')

    def get_a_d_m(self):
        return self.date.strftime('%a %d %b')


class Tables(models.Model):
    start_date = models.DateField('Начало турнира')
    end_date = models.DateField('Окончание турнира', null=True)
    tournament = models.ForeignKey('Tournaments', on_delete=models.CASCADE, verbose_name="Турнир")
    update_date = models.DateField('Обновление данных таблицы', null=True)


class TablesView(models.Model):
    id = models.PositiveBigIntegerField(primary_key=True)
    name = models.CharField('Название команды', max_length=50)
    count_games = models.DecimalField('Игры', max_digits=2, decimal_places=0)
    wins = models.DecimalField('Победы', max_digits=2, decimal_places=0)
    draws = models.DecimalField('Ничьи', max_digits=2, decimal_places=0)
    loses = models.DecimalField('Поражения', max_digits=2, decimal_places=0)
    goal_for = models.DecimalField('Забитые голы', max_digits=3, decimal_places=0)
    goal_against = models.DecimalField('Пропущенные голы', max_digits=3, decimal_places=0)
    goal_difference = models.DecimalField('Разница мячей', max_digits=3, decimal_places=0)
    pts = models.DecimalField('Очки', max_digits=3, decimal_places=0)
    table = models.ForeignKey('Tables', on_delete=models.CASCADE)
    q_we = models.BooleanField('Наша ли команда?', default=False)

    class Meta:
        managed = False
        db_table = 'table_tournaments'