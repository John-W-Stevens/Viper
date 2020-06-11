# Viper CLI

### Command Line Interface tool for launching an ASP.NET Core web application with a MySql Database using Entity Framework.

### Quick start:
    clone the repo: https://github.com/John-W-Stevens/Viper.git
    run viper.py in the same directory you wish to start your ASP.NET project

### What does it do?
Viper allows you to quickly launch an ASP.NET Core MVC, no-https, web application through the command line. It brings in Entity Framework and facilitates the quick configuration of multiple models/schemas (i.e. you can create new models, add attributes, validations, change the display name, and/or designate which attributes are required.) The optional login/registration feature will build out a User Model and LoginUser ViewModel, corresponding Registration and Login Partials, and functional Controller methods that handle the creation of new users and authentication of login attempts. It removes some of the default features related to cookies. In list form, Viper does the following:

- Creates a new ASP.NET MVC no-https web framework
- Initializes Git
- Inputs user MySql credentials (database, username, password) in appsettings.json and then puts appsettings.json into .gitignore
- Brings in session as a service in Startup.cs and injects it into Home.Controller
- Configures Startup.cs to use Session and Entity Framework
- Brings in Entity Framework, sets up Context.cs and injects Context class into project Controller
- Creates multiple models/schemas, based on user input, with customizable fields:
    - add properties/attributes
    - add validations
    - configure display name)
- Provides an optional ready-made login and registration feature which has the following elements:
    - User.cs class (which will go into the database)
    - LoginUser.cs class (a viewModel class that won't go into the database)
    - RegistrationPartial.cshtml (handles input validation and displays error messages)
    - LoginPartial.cshtml (handles input validation and displays error messages)
    - Create(), Login(), Logout() methods added to Home.Controller
    - Passwords hashed and salted with Microsoft.AspNetCore.Identity
- Optional ability to run migrations immediately
- Launches project with dotnet watch run

### Important Notes:
- Viper is highly specific. It is built for .NET 2.2, not 3.0. This program will create a global.json file in the parent directory
    specifiying the use of sdk 2.2.107 (which is necessary if you have multiple versions of .NET like I do).
- Viper will automatically add SchemaId key fields and CreatedAt/UpdatedAt fields to each model created

### Use it Repeatedly:
Rather than manually bringing viper.py into every project I start I put viper.py in my root directory and call it with a terminal command. In order to do this, I added the following function to my ./zshrc file:
```
viper(){
    cp ~/viper.py ./
    python3 viper.py
    rm -rf viper.py
}
```
Now this program is accessbily with the terminal command: viper

Thanks for reading. Hopefully this project will prove useful to someone other than myself. 

Final Note - This is very much a work in progress. If you find a bug (of which there are probably many), please let me know.
