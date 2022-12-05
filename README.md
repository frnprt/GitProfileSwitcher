# Git Profile Switcher
## Introduction
Git Profile Switcher (gitps) is a little personal project to keep multiple ```user.name``` and ```user.email``` at hand. 

It allows to instantly switch to a preset of git profile without having to manually rewrite them every time.

It is mainly targeted to those devs who prefer to have many different accounts/emails and want to use different profile in commits depending on the origin domain.
The program has been made completely interactive via the Python [inquirer](https://github.com/magmax/python-inquirer) package.

## Installation
* Install the inquirer package:<br>
```
pip install inquirer
```
* Download the repository via `git clone` or download as a zip.
* Run the program:
```
python3 path/to/git_profile_switcher.py
```
This will also create a `.gitps_config.ini` file in your home directory.
* Eventually, you can create an alias in your favourite shell. For instance, in `bash` you can execute the following command:
```
echo "# Add alias for gitps\nalias gitps=\042python3 /path/to/GitProfileSwitcher/git_profile_switcher.py\042" >> $HOME/.bashrc
```

## Usage
During execution, the program will first show the currently set `user.name` and `user.email`.

It will then ask the user to choose a course of action.
- `Switch git profile`: starts the process to switch the current `user.name` and `user.email` with previously stored profile. <br> Those will be saved with the `--global` option. If you have no profiles stored in the configuration, the program will abort execution.
- `Setup new git profile`: starts the process to add a new profile to the program configuration. If you already have profile for a given domain or a given entry in a domain, the program will ask you if you want to override them with the new ones.
- `Erase git profile`: starts the process to erase an existing profile from configuration. <br> If you have no profile stored, the program will abort execution.

## Populating the configuration file
The configuration file follows the classic `.ini` format (more on it [here](https://en.wikipedia.org//wiki/INI_file)).

To add a new profile to the config you can either use the built-in helper or you can edit your `gitps_config.ini` directly.

### 1) Using the built-in helper
Assuming you have aliased the command `gitps`:
- Execute `gitps`;
- From the inquirer interface, choose `Setup new git profile`;
- Insert the domain name you want to associate the profile to (e.g `github.com`);
- Insert the name you want the entry to be saved with in the config file. <br> This can be any word you associate to that particular profile;
- Insert your `user.name`;
- Insert your `user.email`;

### 2) Editing the config file
The configuration file is stored in your home directory.
You can add or remove entries following the `.ini` file format.
The interpretation of the file is as follows:
- Domains are stored as [sections](https://en.wikipedia.org//wiki/INI_file#Sections);
- Entry names are stored as [keys](https://en.wikipedia.org//wiki/INI_file#Keys_(properties));
- The `user.name` and `user.email` are concatenated with a `"` character and the resulting string is assigned as value of the corresponding entry key. <br> The reasoning behind the choice of the quote character as separator is simple.
    1) First, most of the git hosting sites do not accept that in a username.
    2) Second, as per [RFC 5321](https://www.rfc-editor.org/rfc/rfc5321) - page 42: 

        > [...] a host that expects to receive mail SHOULD avoid defining mailboxes where the Local-part requires (or uses) the Quoted-string form [...]

    In any case, most of the mail providers directly forbid the `"` character in the local part of the address.

An example of correctly set `gitps_config.ini` is:
```
[github.com]
personal = myusername"myuseremail@example.com
university = myuniversityname"myuniversityemail@mail.com

[anotherdomain.io]
personal = anothername"anothermail@example.com
```
## Erasing stored profile
You can either use the guided process via the `Erase git profile` option or edit the `.ini` file directly.

It's worth noting that, if you delete an entry with the program built-in interface, it will also delete the corresponding domain section if the deleted entry was the only one associated with it.

## Uninstallation
Just delete the folder where you cloned the repo and manually delete the `.ini` file in your home directory.