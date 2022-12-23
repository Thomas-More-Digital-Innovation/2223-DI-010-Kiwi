from django.apps import AppConfig


class KeytrackerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'keyTracker'

    def ready(self):
        from keyTracker.models import Key
        # put your startup code here

        queryset = Key.objects.filter(id=1)

        # making sure there is at least one key in the db
        if queryset:
            print("apps.py: Key table not empty")
        else:
            print("apps.py: Key table empty")
            print("apps.py: making new key object")
            key = Key(keyHolder=None, isReturned=True)
            key.save()
            print(f"apps.py: Key.objects: {Key.objects}")
            print("apps.py: added starterkey")

        print("apps.py: Startup code ran")
