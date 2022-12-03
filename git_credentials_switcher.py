import configparser
import os
import sys
from pathlib import Path

import inquirer

# Show current credentials
print()
print("! Current credentials:")
os.system("echo USERNAME: `git config user.name`")
os.system("echo EMAIL: `git config user.email`")
print()
# Ask for command
questions = [
    inquirer.List('action',
                  message="What do you need to do?",
                  choices=['Switch git credentials',
                           'Setup new git credentials', 'Erase git credentials'],
                  ),
]
answers = inquirer.prompt(questions)
action = answers["action"]

# Initialize the parser for the persistent configuration file
config = configparser.ConfigParser()
prefix = home = str(Path.home())
config.read(home + "/.gitcs_config.ini")
domains = config.sections()

# Take an action based on the previous answer
match action:
    case "Switch git credentials":
        # Check that there is at least one domain registered in the config
        if domains.__len__() == 0:
            print("! You have no credentials stored.\n" +
                  "! Add some with the \"Setup new git credentials\" option and retry")
            sys.exit(-1)
        else:
            # If there is one, ask which to browse
            questions = [
                inquirer.List('domain',
                              message="Select the domain you want to switch the credentials for:",
                              choices=domains,
                              ),
            ]
            answers = inquirer.prompt(questions)
            domain = answers['domain']
            # Check that the selected domain has at least one entry 
            if config[domain].__len__() == 0:
                print("! You have no credentials stored for the selected domain.\n" +
                      "! Add some with the \"Setup new git credentials\" option and retry")
                sys.exit(-1)
            # If it does, ask which to write in .gitconfig
            questions = [
                inquirer.List('entry',
                              message="Select the git credentials to switch to:",
                              choices=config[domain],
                              ),
            ]
            answers = inquirer.prompt(questions)
            entry = answers['entry']
            values = config.get(domain, entry).split("\"")
            name = values[0]
            email = values[1]
            os.system("git config --global user.name \"" + name + "\"")
            os.system("git config --global user.email \"" + email + "\"")
            print("Successfully switched credentials.")
            sys.exit(0)

    case "Setup new git credentials":
        # Ask for domain and entry name
        print("! NOTE: Refrain from using the \" and = characters in any input field.")
        domain = input("Domain name [e.g. \"github.com\"]: ")
        if "=" in domain or "\"" in domain:
                print("! The [\"=] characters are not allowed.\n" +
                      "! Please consider changing your username for the selected domain and/or changing/aliasing your email address.")
                sys.exit(-1)
        entry = input("Entry name [e.g. \"university-account\"]: ")
        if "=" in entry or "\"" in entry:
                print("! The [\"=] characters are not allowed.\n" +
                      "! Please consider changing your username for the selected domain and/or changing/aliasing your email address.")
                sys.exit(-1)
        # If the domain already exists in the config:
        if config.has_section(domain):
            print("! The domain already exists in the config.\n")
            # Check if the entry exists too
            if config.has_option(domain, entry):
                # If it does, ask to proceed with overwrite
                print("! The selected domain already has an entry with the same name.\n")
                overwrite = input("! Do you want to overwrite it [y/N]? ")
                # If not, abort the operation
                if overwrite.strip() != "y":
                    print("Aborting operation...")
                    sys.exit(-1)
            print("! The new credentials will be added to the existing domain...")
        # Else, add it to the config
        else:
            config.add_section(domain)
        # Ask for the name and email to store in the entry
        name = input("user.name: ")
        email = input("user.email: ")
        if "=" in name or "\"" in name:
                print("! The [\"=] characters are not allowed.\n" +
                      "! Please consider changing your username for the selected domain and/or changing/aliasing your email address.")
                sys.exit(-1)
        if "=" in email or "\"" in email:
                print("! The [\"=] characters are not allowed.\n" +
                      "! Please consider changing your username for the selected domain and/or changing/aliasing your email address.")
                sys.exit(-1)
        config.set(domain, entry, name + "\"" + email)
        with open(home + '/.gitcs_config.ini', 'w') as configfile:
            config.write(configfile)
            print("New credentials successfully stored.")
            sys.exit(0)

    case "Erase git credentials":
        # Check that there is at least one domain registered in the config
        if domains.__len__() == 0:
            print("! You have no credentials stored.\n" +
                  "! Add some with the \"Setup new git credentials\" option and retry")
            sys.exit(-1)
        else:
            # If there is one, ask which to browse
            questions = [
                inquirer.List('domain',
                              message="Select the domain you want to switch the credentials for:",
                              choices=domains,
                              ),
            ]
            answers = inquirer.prompt(questions)
            domain = answers['domain']
            # Check that the selected domain has at least one entry
            if config[domain].__len__() == 0:
                print("! You have no credentials stored for the selected domain.\n" +
                      "! Add some with the \"Setup new git credentials\" option and retry")
                sys.exit(-1)
            # If it does, ask to select which is going to be deleted
            questions = [
                inquirer.List('entry',
                              message="Select the git credentials to switch to:",
                              choices=config[domain],
                              ),
            ]
            answers = inquirer.prompt(questions)
            entry = answers['entry']
            # Delete the selected entry and write to file
            config.remove_option(domain, entry)
            # If that was the last entry of the domain, delete the domain
            if config[domain].__len__ == 0:
                config.remove_section(domain)
            with open(home + '/.gitcs_config.ini', 'w') as configfile:
                config.write(configfile)
                print("Credentials successfully erased.")
                sys.exit(0)
