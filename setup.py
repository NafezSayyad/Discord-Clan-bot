'''Entrypoint'''
from os import getenv
from dotenv import load_dotenv

def main():
    # In case it is a production environment, the .env file should be ignored
    # Variables in production should be stored somewhere else (e.g. GitHub secrets)
    if getenv("ENV")!="PROD":
        load_dotenv()
    from setup import bot

    from Commands import help, teams, join, about, socials, createRole
    import events
    from events import welcomemessage, nameChange
    TOKEN=getenv("TOKEN")
    bot.run(TOKEN)

if __name__=="__main__":
    main()