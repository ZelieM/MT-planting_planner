from django.db import models


class ResearchMember(models.Model):
    # Model used to create a permission for research team they are the only one who can access this application
    # https://stackoverflow.com/a/37988537/7177417
    class Meta:
        managed = False
        permissions = (
            ("is_researcher", "Can access research interface"),
        )
