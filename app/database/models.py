from tortoise import fields, models

class User(models.Model):
    id = fields.IntField(pk=True)
    tg_id = fields.BigIntField(unique=True)
    name = fields.CharField(max_length=30)
    number = fields.CharField(max_length=12)
    username = fields.CharField(max_length=30, null=True)
    block = fields.BooleanField(default=False)

    class Meta:
        table = "users"