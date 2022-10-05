from django.apps import AppConfig


class KeytrackerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'keyTracker'

    def ready(self):
        from keyTracker.models import Key
        # put your startup code here

        queryset = Key.objects.filter(id=1)

        if queryset:
            print("Key table not empty")
        else:
            print("Key table empty")
            print("making new key object")
            key = Key(keyHolder=None, isReturned=True)
            key.save()
            print(f"Key.objects: {Key.objects}")
            print("added starterkey")

        print("Startup code ran")
