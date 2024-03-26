from django.contrib import admin
from .models import Memories, Congratulations


@admin.register(Memories)
class MemoriesAdmin(admin.ModelAdmin):
    pass


@admin.register(Congratulations)
class CongratulationsAdmin(admin.ModelAdmin):
    pass