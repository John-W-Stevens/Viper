# Viper CLI

### Command Line Interface tool for launching an ASP.NET Core web application with a MySql Database using Entity Framework.

### Quick start:
    clone the repo: https://github.com/John-W-Stevens/Viper.git
    run viper.py in the same directory you wish to start your ASP.NET project

### What does it do?
Viper allows you to quickly launch an ASP.NET Core MVC, no-https, web application through the command line. It bring in Entity Framework and facilitates the quick configuration of multiple models/schemas (i.e. you can create new models, add attributes, validations, change the display name, and/or designate which attributes are required.) It removes some of the default features related to cookies. In list form, Viper does the following:

- Creates a new ASP.NET MVC framework
- Initializes Git
- Inputs user MySql credentials (database, username, password) in appsettings.json and then puts appsettings.json into .gitignore
- Brings in Entity Framework, sets up Context.cs and injects Context class into project Controller
- Sets up Startup.cs (Bring in entity framework, removes cookies)
- Creates multiple models/schemas with customizable fields (add properties/attributes, validations, configure display name)
- Launches project with dotnet watch run

### Important Notes:
- Viper is highly specific. I built this for .NET 2.2, not 3.0. This program will create a global.json file in the parent directory
    specifiying the use of sdk 2.2.107 (which is necessary if you have multiple versions of .NET like I do).
- I made this specifically for MVC no-https projects

Thanks for reading. Hopefully this project will prove useful to someone other than myself. 

Final Note - This is very much a work in progress. If you find a bug (of which there are probably many), please let me know.