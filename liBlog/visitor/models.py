from datetime import timedelta
from django.utils import timezone
import logging
import traceback

# from django.contrib.gis.geoip import GeoIP, GeoIPException

try:
    from django.conf import settings
    User = settings.AUTH_USER_MODEL
except AttributeError:
    from django.conf import settings
    from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext, ugettext_lazy as _
from . import utils

USE_GEOIP = getattr(settings, 'TRACKING_USE_GEOIP', False)
CACHE_TYPE = getattr(settings, 'GEOIP_CACHE_TYPE', 4)

log = logging.getLogger('tracking.models')


class VisitorManager(models.Manager):
    def active(self, timeout=None):
        """
        Retrieves only visitors who have been active within the timeout
        period.
        """
        if not timeout:
            timeout = utils.get_timeout()

        now = timezone.now()
        cutoff = now - timedelta(minutes=timeout)

        return self.get_queryset().filter(last_update__gte=cutoff)


class Visitor(models.Model):
    session_key = models.CharField(max_length=40)
    ip_address = models.CharField(max_length=20)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True)
    user_agent = models.CharField(max_length=255)
    referrer = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    page_views = models.PositiveIntegerField(default=0)
    session_start = models.DateTimeField(default=timezone.now)
    last_update = models.DateTimeField(default=timezone.now)

    objects = VisitorManager()

    # def __init__(self, *args, **kwargs):
    #     super(Visitor, self).__init__(*args, **kwargs)
    #     self.session_start = timezone.now()
    #     self.last_update = timezone.now()

    def _time_on_site(self):
        """
        Attempts to determine the amount of time a visitor has spent on the
        site based upon their information that's in the database.
        """
        if self.session_start:
            seconds = (self.last_update - self.session_start).seconds

            hours = seconds / 3600
            seconds -= hours * 3600
            minutes = seconds / 60
            seconds -= minutes * 60

            return u'%i:%02i:%02i' % (hours, minutes, seconds)
        else:
            return ugettext(u'unknown')

    time_on_site = property(_time_on_site)

    def __str__(self):
        username = self.user.username if hasattr(self.user, 'username') else '未登录'
        return u'{0} at {1} '.format(
            username,
            self.ip_address
        )

    class Meta:
        ordering = ('-last_update',)
        unique_together = ('session_key', 'ip_address',)


class UntrackedUserAgent(models.Model):
    keyword = models.CharField(_('keyword'), max_length=100, help_text=_(
        'Part or all of a user-agent string.  For example, "Googlebot" here will be found in "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)" and that visitor will not be tracked.'))

    def __str__(self):
        return self.keyword

    class Meta:
        ordering = ('keyword',)
        verbose_name = _('Untracked User-Agent')
        verbose_name_plural = _('Untracked User-Agents')


class BannedIP(models.Model):
    ip_address = models.GenericIPAddressField('IP Address', help_text=_(
        'The IP address that should be banned'))

    def __str__(self):
        return self.ip_address

    class Meta:
        ordering = ('ip_address',)
        verbose_name = _('Banned IP')
        verbose_name_plural = _('Banned IPs')
