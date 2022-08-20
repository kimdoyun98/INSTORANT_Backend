from django.contrib.auth.models import models


class UserFavorite(models.Model):
    username = models.OneToOneField('UserInfomation', models.DO_NOTHING, db_column='username', primary_key=True)
    favor_id = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'user_favorite'
        unique_together = (('username', 'favor_id'),)


class UserInfomation(models.Model):
    username = models.CharField(primary_key=True, max_length=30)
    password = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_infomation'


class UserReview(models.Model):
    review_id = models.AutoField(primary_key=True)
    username = models.ForeignKey(UserInfomation, models.DO_NOTHING, db_column='username')
    restaurant_id = models.CharField(max_length=30)
    content = models.TextField(blank=True, null=True)
    image1 = models.CharField(max_length=255, blank=True, null=True)
    image2 = models.CharField(max_length=255, blank=True, null=True)
    image3 = models.CharField(max_length=255, blank=True, null=True)
    score = models.IntegerField(blank=True, null=True)
    date_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'user_review'
