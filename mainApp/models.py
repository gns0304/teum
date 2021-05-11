from django.db import models
from django.conf import settings

# Create your models here.

User = settings.AUTH_USER_MODEL

PLATFORM = (
    (1, "상행선"),
    (2, "하행선")
)


class Station(models.Model):

    line = models.CharField(max_length=6, null=False, blank=False, verbose_name="호선")
    name = models.CharField(max_length=10, null=False, blank=False, verbose_name="역명")
    foothold = models.BooleanField(default=False, null=False, blank=False, verbose_name="발판 유무")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "역 정보 관리"
        verbose_name = "역 정보"


class Door(models.Model):

    station = models.ForeignKey(Station, on_delete=models.CASCADE, verbose_name="역 정보")
    platform = models.PositiveSmallIntegerField(null=False, blank=False, choices=PLATFORM, verbose_name="승강장번호")
    car_number = models.PositiveSmallIntegerField(null=False, blank=False, verbose_name="차량순서")
    door_number = models.PositiveSmallIntegerField(null=False, blank=False, verbose_name="차량출입문번호")
    distance = models.DecimalField(max_digits=3, decimal_places=1, verbose_name="안전거리")

    class Meta:
        verbose_name_plural = "안전거리 정보 관리"
        verbose_name = "안전거리 정보"


class Complexity(models.Model):

    DAY = (
        (1, "평일"),
        (2, "토요일"),
        (3, "일요일")
    )

    station = models.ForeignKey(Station, on_delete=models.CASCADE, verbose_name="역 정보")
    platform = models.PositiveSmallIntegerField(null=False, blank=False, choices=PLATFORM, verbose_name="승강장번호")
    day = models.PositiveSmallIntegerField(null=False, blank=False, choices=DAY, verbose_name="요일")

    def __str__(self):
        return "{}_{}_{}".format(self.station.name, self.get_platform_display(), self.get_day_display())

    class Meta:
        verbose_name_plural = "혼잡도 정보 관리"
        verbose_name = "혼잡도 정보"

class Time(models.Model):

    complex_id = models.ForeignKey(Complexity, on_delete=models.CASCADE, verbose_name="혼잡도 정보")
    time = models.TimeField(null=False, blank=True,verbose_name="시간")
    complexity = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="혼잡도")

    class Meta:
        verbose_name_plural = "혼잡도 시간정보 관리"
        verbose_name = "혼잡도 시간정보"


class FavoriteStation(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="계정 정보")
    station = models.ForeignKey(Station, on_delete=models.CASCADE, verbose_name="즐겨 찾는 역")

    class Meta:
        verbose_name_plural = "즐겨 찾는 역 정보 관리"
        verbose_name = "즐겨 찾는 역 정보"