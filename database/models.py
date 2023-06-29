from tortoise import Model, fields


class User(Model):
    id = fields.IntField(pk=True)
    uid = fields.IntField(unique=True)
    name = fields.CharField(max_length=50, null=True, unique=True)
    points = fields.FloatField(default=0)
    registered = fields.BooleanField(default=False)
    twitter_username = fields.CharField(max_length=30, null=True)
    instagram_username = fields.CharField(max_length=30, null=True)
    banned_until = fields.DatetimeField(null=True)
    already_followed_instagram = fields.BooleanField(default=False)
    already_followed_twitter = fields.BooleanField(default=False)
    confirmed = fields.BooleanField(default=False)
    confirmed_username = fields.CharField(max_length=50, null=True, unique=True)
    bsc = fields.CharField(max_length=100, null=True, unique=True)

    class Meta:
        table = 'users'


class Admins(Model):
    id = fields.IntField(pk=True)
    uid = fields.IntField(null=True)
    username = fields.CharField(max_length=100, null=True)

    class Meta:
        table = 'admins'


class Contest(Model):
    id = fields.IntField(pk=True)
    server_name = fields.CharField(max_length=100, null=True)
    contest_name = fields.CharField(max_length=100, null=True)
    point_name = fields.CharField(max_length=100, null=True)
    manual_contest_status = fields.CharField(max_length=20, null=True)
    registration_status = fields.BooleanField(default=False)
    check_score = fields.BooleanField(default=False)
    give_points = fields.BooleanField(default=False)
    transfer_points = fields.BooleanField(default=False)
    contest_start_date = fields.CharField(max_length=100, null=True)
    contest_end_date = fields.CharField(max_length=100, null=True)

    class Meta:
        table = 'contest'


class AdminPreferences(Model):
    id = fields.IntField(pk=True)
    twitter_api_key = fields.CharField(max_length=150, null=True)
    instagram_api_ley = fields.CharField(max_length=150, null=True)
    twitter_hashtags = fields.CharField(max_length=150, null=True)
    instagram_hashtags = fields.CharField(max_length=150, null=True)
    retweet = fields.FloatField(default=0)
    quote_tweet = fields.FloatField(default=0)
    tweet_like = fields.FloatField(default=0)
    twit_tagged = fields.FloatField(default=0)
    hashtag_t = fields.FloatField(default=0)
    twit_follow = fields.FloatField(default=0)
    ig_like = fields.FloatField(default=0)
    ig_comment = fields.FloatField(default=0)
    ig_follow = fields.FloatField(default=0)
    hashtag = fields.FloatField(default=0)
    sent_message = fields.FloatField(default=0)
    react = fields.FloatField(default=0)
    voice = fields.FloatField(default=0)

    class Meta:
        table = 'admin_preferences'