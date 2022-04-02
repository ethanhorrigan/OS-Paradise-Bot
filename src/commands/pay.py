'''Pay module'''
from src.settings import get_date_now, MOD, get_permissions
from src.commands.base_command  import BaseCommand
import src.database.database as db

class Pay(BaseCommand):
    '''Pay command for SOTW/BOTW payments'''

    def __init__(self):
        description = 'Payment for SOTW/BOTW'
        params = ['recipient', 'amount']
        super().__init__(description, params, MOD)

    async def handle(self, params, message, client):
        valid_amounts = ['1m', '3m', '6m']
        mod = str(message.author.display_name)
        recipient = str(params[0])
        amount = str(params[1]).lower()
        date = str(get_date_now())
        permissions = str(message.author.display_name)
        if get_permissions(permissions) != MOD:
            print(message.author.display_name+ ': not a mod.')
            return
        if str(message.channel.name) != '💰beach-bank':
            return
        if amount not in valid_amounts:
            return await message.channel.send(message.author.mention+' \
                Please enter 1m, 3m or 6m')
        try:
            image_url = message.attachments[0].url
        except IndexError:
            return await message.channel.send(message.author.mention+' \
                Please attach an image to verify payout.')
        db.insert_payments(mod, recipient, amount, date, image_url)


        await message.channel.send('\n'+message.author.mention+' \
            \nPaid: '+recipient+' \nAmount: '+ amount)
