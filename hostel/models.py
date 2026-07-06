from django.db import models


class Hostel(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    total_rooms = models.PositiveIntegerField()

    class Meta:
        db_table = "hostel"
        ordering = ["name"]

    def __str__(self):
        return self.name


class HostelRoom(models.Model):
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE)
    room_no = models.CharField(max_length=20)
    capacity = models.PositiveIntegerField()
    current_occupancy = models.PositiveIntegerField()

    class Meta:
        db_table = "hostel_room"
        ordering = ["room_no"]

    def __str__(self):
        return f"{self.hostel.name} - {self.room_no}"