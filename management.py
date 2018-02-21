import requests

from utils import fileIO

class APIUnavailable(Exception):
    pass

class TwitchAPI:

    def twitchAPIGet(self, endpoint, params):
        api_client_id = fileIO.load_json("settings.json")["api_client_id"]
        if api_client_id != "":
            url = "https://api.twitch.tv/helix" + endpoint #endpoint starts with /
            headers = {"Client-ID":api_client_id} #set header with client id for access
            r = requests.get(url, params=params, headers=headers)
            apiResponseJson = r.json()
            return apiResponseJson
        else:
            raise APIUnavailable()

class CommandCreation:

    def __init__(self):
        #Create list of commands
        self.commands = []
        self.commands.append(self._quit)
        self.commands.append(self._generate_add_user_command)
        self.commands.append(self._remove_user)
        self.commands.append(self._list_users)
        self.commands.append(self._edit_user)
        self.commands.append(self._listen)
        self.commands.append(self._unlisten)
        self.commands.append(self._list_settings)
        self.commands.append(self._edit_setting)
        #See if settings files need to be generated
        if fileIO.load_json("settings.json") == None: #If settings file not exist
            self._generate_settings()
        if fileIO.load_json("users.json") == None: #If users file not exist
            self._generate_users()

    def menu(self):
        """Function for menu system"""
        self.loop = True
        while self.loop == True: #Loop until quitting
            print("Please enter the number of the command you would like to run.")
            print("0. Quit, 1. Add User, 2. Remove User, 3. List Users, 4. Edit User, 5. Listen, 6. Unlisten, 7. List Settings, 8. Edit Setting")
            option = input()
            try: #Try to convert input to int and run command
                option = int(option)
                command = self.commands[option]() #Run command
                if command != None: #if command returned
                    with open("commands.txt", "a") as f:
                        f.write(command)
            except (ValueError, IndexError): #If invalid input
                pass

    def _generate_settings(self):
        """Function to generate settings.json"""
        settings = {}
        settings["api_client_id"] = input("(OPTIONAL) Please enter your Twitch API Client ID: ") #Get API Client ID first so I can use API to get user ID
        #Save JSON
        fileIO.save_json("settings.json", settings)
        name = False
        while not name: #While name not set
            name = input("Please enter the username of your Twitch account: ").lower()
            userID = self._get_user_id(name)
            if not userID:
                name = False
        settings["userid"] = userID
        settings["oauth"] = input("Please enter the oauth token for your Twitch account: ")
        if settings["oauth"].startswith("oauth:"): #If the oauth token starts with oauth:, remove it
            settings["oauth"] = settings["oauth"][6:]
        settings["error_webhook"] = input("Please enter the Discord WebHook URL you would like errors to be sent to: ")
        #Save JSON
        fileIO.save_json("settings.json", settings)

    def _generate_users(self):
        """Function to generate users.json"""
        users = {}
        args = self._add_user()
        #Grab info from args
        users[args["userID"]] = {}
        users[args["userID"]]["name"] = args["name"]
        users[args["userID"]]["webhook_url"] = args["webhook_url"]
        users[args["userID"]]["blacklist"] = args["blacklist"]
        #Try to grab override info, default to blank if doesn't exist
        users[args["userID"]]["override_user"] = args.get("overrideUser", "")
        users[args["userID"]]["override_userid"] = args.get("overrideUserID", "")
        users[args["userID"]]["override_oauth"] = args.get("overrideOauth", "")
        fileIO.save_json("users.json", users)

    def _list_users(self):
        """Function to list users and settings per user"""
        users = fileIO.load_json("users.json")
        print("The list of users is as follows:")
        for i in users:
            print(users[i]["name"])
        self._list_user_settings(users)        

    def _list_user_settings(self, users):
        """Function to list all settings of a specific user"""
        name  = False
        while not name: #Loop until they type a valid input
            option = input("Please enter the name of the user you would like to view the settings of: ").lower()
            userID = self._get_user_id(name)
            try: #Try to print settings for user
                print("The list of settings for user {0} is:")
                for i in users[userID]:
                    print("{0}: {1}".format(i, users[userID][i]))
            except KeyError: #if user valid Twitch user but not in bot, exit back to menu
                print("That user is not in the bot, try adding it.")
                return(None)
        return(userID)

    def _edit_user(self):
        """Function to create edit_user command for bot"""
        users = fileIO.load_json("users.json")
        print("The list of users is as follows: ")
        for i in users:
            print(users[i]["name"])
        #List specific user's settings and get user id
        userID = self._list_user_settings(users)
        #Loop until valid option given
        option = False
        while not option:
            option = input("Please enter the setting you would like to change: ")
            if option not in users[userID]:
                option = False
                print("That setting is not valid.")
        #Get input for new setting
        args = input("Please enter what you would like to change that setting to: ")
        #Output
        command = "edit_user {0} {1} {2}\r\n".format(userID, option, args)
        return(command)

    def _add_user(self):
        """Function to get user input for adding user to bot"""
        args = {}
        args["name"] = False
        #Loop until valid name given
        while not args["name"]: #While name not set
            args["name"] = input("Please enter the username of the user you would like to add: ").lower()
            args["userID"] = self._get_user_id(args["name"])
            if not args["userID"]:
                args["name"] = False
        #Get more input
        args["webhook_url"] = input("Please enter the Discord WebHook URL for this user: ")
        args["override"] = None
        #Loop until override info completed
        while args["override"] == None:
            userInput = input("Override authentication user? y/n: ")
            if userInput.lower() == "y":
                args["override"] = True
                args["overrideUser"] = False
                #Loop until valid user given
                while not args["overrideUser"]:
                    args["overrideUser"] = input("Please enter the Twitch username that you would like to authenticate with: ").lower()
                    args["overrideUserID"] = self._get_user_id(args["overrideUser"])
                    if not args["overrideUserID"]:
                        args["overrideUser"] = False
                #Get oauth input, removing 'oauth:' from beginning
                args["overrideOauth"] = input("Please enter the oauth token for the Twitch account, omitting 'oauth:': ")
                if args["overrideOauth"].startswith("oauth:"): #If the oauth token starts with oauth:, remove it
                    args["overrideOauth"] = args["overrideOauth"][6:]
            elif userInput.lower() == "n":
                args["override"] = False
            else:
                print("That is not a valid input.")
        args["blacklist"] = input("Please enter a space separated list of users to blacklist: ")
        return(args)
        
    def _generate_add_user_command(self):
        """Function to generate command string for add_user"""
        args = self._add_user()
        #Create command string
        command = "add_user {0} {1} {2}".format(args["userID"], args["name"], args["webhook_url"])
        if args["override"]:
            command += " override {0} {1} {2}".format(args["overrideUserID"], args["overrideUser"], args["overrideOauth"])
        if args["blacklist"] != "":
            command += " {0}".format(args["blacklist"])
        command += "\r\n"
        return(command)

    def _remove_user(self):
        """Function to create remove_user command for bot"""
        name = False
        while not name: #While name not set
            name = input("Please enter the username of the user you would like to remove: ").lower()
            userID = self._get_user_id(name)
            if not userID:
                name = False
        command = "remove_user {0}\r\n".format(userID)
        return(command)

    def _list_settings(self, settings=None):
        """Function to list all settings"""
        if settings == None:
            settings = fileIO.load_json("settings.json")
        print("The list of settings is: ")
        for i in settings:
            print("{0}: {1}".format(i, settings[i]))
        return(None)

    def _edit_setting(self):
        """Function to create edit_setting command"""
        settings = fileIO.load_json("settings.json")
        self._list_settings(settings=settings)
        option = False
        while not option: #While loop until valid setting given
            option = input("Please type the setting you would like to change: ")
            if option not in settings:
                option = False
        newSetting = input("Please enter what you would like to change that setting to: ")
        command = "edit_setting {0} {1}".format(option, newSetting)
        return(command)

    def _listen(self):
        """Function to create listen command"""
        users = fileIO.load_json("users.json")
        print("The list of users is: ")
        for i in users:
            print(users[i]["name"])
        name = False
        while not name: #Loop until valid user given
            name = input("Please enter the user that you would like to start listening to events for: ")
            userID = self._get_user_id(name)
            if not userID:
                name = False
        #Output
        command = "listen {0}".format(userID)
        return(command)

    def _unlisten(self):
        """Function to create unlisten command"""
        users = fileIO.load_json("users.json")
        print("The list of users is: ")
        for i in users:
            print(users[i]["name"])
        name = False
        while not name: #Loop until valid name given
            name = input("Please enter the user that you would no longer like to be listening to events for: ")
            userID = self._get_user_id(name)
            if not userID:
                name = False
        #Output
        command = "unlisten {0}".format(userID)
        return(command)

    def _get_user_id(self, name):
        """Function to get a user id, either from the API or asking the user if no API access available"""
        try:
            apiResponse = twitchAPI.twitchAPIGet("/users", {"login": name}) #Try to get user id from API
            userID = apiResponse["data"][0]["id"]
        except (KeyError, APIUnavailable):
            userID = input("Please enter the user id of the user: ")
        except IndexError: #If Twitch API does not return user id
            print("That user does not exist on Twitch.")
            userID = False
        return(userID)

    def _quit(self):
        self.loop = False

if __name__ == "__main__":
    twitchAPI = TwitchAPI()
    commands = CommandCreation()
    commands.menu()