from settings import get_date_now, MOD, get_permissions
from commands.base_command  import BaseCommand
import database.database as db

class Pay(BaseCommand):

    def __init__(self):
        # A quick description for the help message
        description = "Payment for SOTW/BOTW"
        # A list of parameters that the command will take as input
        # Parameters will be separated by spaces and fed to the 'params' 
        # argument in the handle() method
        # If no params are expected, leave this list empty or set it to None
        params = ['recipient', 'amount']
        super().__init__(description, params, MOD)

    # Override the handle() method
    # It will be called every time the command is received
    async def handle(self, params, message, client):
        # 'params' is a list that contains the parameters that the command 
        # expects to receive, t is guaranteed to have AT LEAST as many
        # parameters as specified in __init__
        # 'message' is the discord.py Message object for the command to handle
        # 'client' is the bot Client object
        valid_amounts = ['1m', '3m', '6m']
        mod = str(message.author.display_name)
        # Check Mod to see if valid mod
        # Person receiving 
        recipient = str(params[0])
        # Amount
        amount = str(params[1]).lower()
        # Todays Date 
        date = str(get_date_now())

        # Validate user permissions
        # Check if amount entered is valid
        permissions = str(message.author.display_name)
        if (get_permissions(permissions) != MOD):
            print(message.author.display_name+ ': not a mod.')
            return
        if (str(message.channel.name) != '💰beach-bank'):
            return
        if (amount not in valid_amounts):
            return await message.channel.send(message.author.mention+' Please enter 1m, 3m or 6m')
        try:
            image_url = message.attachments[0].url
        except IndexError:
            return await message.channel.send(message.author.mention+' Please attach an image to verify payout.')
        db.insert_payments(mod, recipient, amount, date, image_url)


        await message.channel.send('\n'+message.author.mention+' \nPaid: '+recipient+' \nAmount: '+ amount)
