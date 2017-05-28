from django.core.management.base import NoArgsCommand, CommandError
from dropbox import DropboxOAuth2FlowNoRedirect

from django_dropbox.settings import CONSUMER_KEY, CONSUMER_SECRET


class Command(NoArgsCommand):

    def handle_noargs(self, *args, **options):
        auth_flow = DropboxOAuth2FlowNoRedirect(CONSUMER_KEY, CONSUMER_SECRET)

        authorize_url = auth_flow.start()
        self.stdout.write('1. Go to: {}'.format(authorize_url))
        self.stdout.write('2. Click "Allow" (you might have to log in first).')
        self.stdout.write('3. Copy the authorization code.')
        auth_code = raw_input("Enter the authorization code here: ").strip()

        try:
            oauth_result = auth_flow.finish(auth_code)
            self.stdout.write("DROPBOX_ACCESS_TOKEN = '{}'".format(oauth_result.access_token))
        except Exception as e:
            raise CommandError('Error: {}'.format(e))
