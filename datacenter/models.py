from django.db import models


class Passcard(models.Model):
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    passcode = models.CharField(max_length=200, unique=True)
    owner_name = models.CharField(max_length=255)

    def __str__(self):
        if self.is_active:
            return self.owner_name
        return f'{self.owner_name} (inactive)'


class Visit(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    passcard = models.ForeignKey(Passcard, on_delete=models.CASCADE)
    entered_at = models.DateTimeField()
    leaved_at = models.DateTimeField(null=True)

    def __str__(self):
        return '{user} entered at {entered} {leaved}'.format(
            user=self.passcard.owner_name,
            entered=self.entered_at,
            leaved=(
                f'leaved at {self.leaved_at}'
                if self.leaved_at else 'not leaved'
            )
        )
        
    def get_duration(self):
      if self.leaved_at:
        delta_time = self.leaved_at - self.entered_at
      else :
        dt_now_0 = datetime.datetime.now()
        delta_time = django.utils.timezone.make_aware(dt_now_0) - self.entered_at

      seconds = delta_time.total_seconds()
      return seconds        


    def is_visit_long(self, minutes=60):
      sec = self.get_duration()
      seconds = int( sec )
      real_minutes = int( seconds / 60)
      return  real_minutes > minutes


def format_duration(seconds):
    hours = int(seconds // 3600 )
    minutes = int( (seconds % 3600) // 60)
    str_delta_time = "{0} ч {1} мин".format(hours,minutes)
    return str_delta_time
