import os
import pathlib

def appsettings_json(project_name, database, username, password):
    # os.system(f"touch ./{project_name}/appsettings.json")
    os.system(f"cat > ./{project_name}/appsettings.json << EOF\n"
            '{\n'
            '    "DBInfo": {\n'
            '    "Name": "MySQLconnect",\n'
            f'    "ConnectionString": "server=localhost;userid={username};password={password};port=3306;database={database};SslMode=None"\n'
            '    }\n'
            '}'
    )

def global_json():
    os.system("touch global.json")
    os.system("cat >> ./global.json << EOF\n"
        '{\n'
        '    "sdk": {\n'
        '        "version": "2.2.107"\n'
        '    }\n'
        '}\n'
    )

def gitignore(project_name):
    os.system(f"touch ./{project_name}/.gitignore")     # add .gitignore
    os.system(f"cat >> ./{project_name}/.gitignore << EOF\n"
              "appsettings.json")

def build_startup_file(project_name, context_name):    
    lines = [
       "using System;",
       "using System.Collections.Generic;",
       "using System.Linq;",
       "using System.Threading.Tasks;",
       "using Microsoft.AspNetCore.Builder;",
       "using Microsoft.AspNetCore.Hosting;",
       "using Microsoft.AspNetCore.Http;",
       "using Microsoft.AspNetCore.Mvc;",
       "using Microsoft.Extensions.Configuration;",
       "using Microsoft.Extensions.DependencyInjection;",
       "",
       "using Microsoft.EntityFrameworkCore;",
       f"using {project_name}.Models;",
       "",
       f"namespace {project_name}",
       "{",
       "    public class Startup",
       "    {",
       "        public Startup(IConfiguration configuration)",
       "        {",
       "            Configuration = configuration;",
       "        }",
       "",
       "        public IConfiguration Configuration { get; }",
       "",
       "        // This method gets called by the runtime. Use this method to add services to the container.",
       "        public void ConfigureServices(IServiceCollection services)",
       "        {",
       "            services.AddSession();",
       f"            services.AddDbContext<{context_name}>(options => options.UseMySql(Configuration[\"DBInfo:ConnectionString\"]));",
       "            services.AddMvc().SetCompatibilityVersion(CompatibilityVersion.Version_2_2);",
       "        }",
       "",
       "        // This method gets called by the runtime. Use this method to configure the HTTP request pipeline.",
       "        public void Configure(IApplicationBuilder app, IHostingEnvironment env)",
       "        {",
       "            if (env.IsDevelopment())",
       "            {",
       "                app.UseDeveloperExceptionPage();",
       "            }",
       "            else",
       "            {",
       "                app.UseExceptionHandler(\"/Home/Error\");",
       "            }",
       "",
       "            app.UseStaticFiles();",
       "            app.UseSession();",
       "            app.UseMvc(routes =>",
       "            {",
       "                routes.MapRoute(",
       "                    name: \"default\",",
       "                    template: \"{controller=Home}/{action=Index}/{id?}\");",
       "            });",
       "        }",
       "    }",
       "}",
       "",
    ]
    
    new_file_contents = ""
    for line in lines:
        new_file_contents += line + "\n"

    os.system(f"cat > ./{project_name}/Startup.cs << EOF\n{new_file_contents}")

def build_context_file(project_name, context_name, models):

    lines = [
       "using System;",
       "using Microsoft.EntityFrameworkCore;",
       "",
       f"namespace {project_name}.Models",
       "{",
       f"    public class {context_name} : DbContext",
       "    {",
       f"        public {context_name}(DbContextOptions options) : base(options) "+"{ }",
       "",
    ]
    for schema in models:
       lines.append(f"        public DbSet<{schema[0]}> {schema[1]} " +"{ get; set; }")

    lines2 = [
       "    }",
       "}",
       "",
    ]
    lines += lines2

    new_file_contents = ""
    for line in lines:
        new_file_contents += line + "\n"
    
    os.system(f"touch ./{project_name}/Models/{context_name}.cs")
    os.system(f"cat > ./{project_name}/Models/{context_name}.cs << EOF\n{new_file_contents}")

def build_models(project_name):

    models = []

    def is_yes(res):
        return res in ["y", "Y", "yes", "Yes", "YES"]

    def build_model(project_name, schema_singular, schema_plural):

        lines1 = [
        "using System;",
        "using System.ComponentModel.DataAnnotations;",
        "",
        f"namespace {project_name}.Models",
        "{",
        f"    public class {schema_singular}",
        "    {",
        "        [Key]",
        f"        public int {schema_singular}Id " +"{ get; set; }",
        "",
        ]

        lines2 = []

        while True:
            res = input("Would you like to add an attribute? ")
            if is_yes(res):
                label = input("What is this attribute called? ")
                stype = input("What is this attribute's type? ")
                required = input("Y/n - Is this attribute required? ")
                display = ""
                while True:
                    change_display = input("Y/n - Would you like to change the default display? ")
                    if is_yes(change_display):
                        d = input("Enter custom display message: ")
                        r = input(f"Y/n - You wrote -- {d} -- as your custom display message. Is this correct? ")
                        if is_yes(r):
                            display = d
                            break
                    else:
                        break

                validations = []
                while True:
                    res = input("Y/n - Would you like to add a validation to this attribute? ")
                    if is_yes(res):
                        validation = input("Please enter your validation exactly as it would appear in C#. For example: [Range(1,5)] ")
                        r = input(f"Y/n - You entered: {validation} as your validation. Is this correct? ")
                        if is_yes(r):
                            validations.append(validation)
                    else:
                        break
                # add attribute
                if required:
                    lines2.append("        [Required]")
                for v in validations:
                    lines2.append(f"        {v}")
                if display != "":
                    lines2.append(f'        [Display(Name = "{display}")]')
                lines2.append(f"        public {stype} {label} " + "{ get; set; }")
                lines2.append("")
            else:
                break

        lines3 = [
        "        [Required]",
        "        public DateTime CreatedAt { get; set; }",
        "",
        "        [Required]",
        "        public DateTime UpdatedAt { get; set; }",
        "    }",
        "}",
        "",
        ]

        lines = lines1 + lines2 + lines3

        new_file_contents = ""
        for line in lines:
            new_file_contents += line + "\n"

        os.system(f"touch ./{project_name}/Models/{schema_singular}.cs")
        os.system(f"cat > ./{project_name}/Models/{schema_singular}.cs << EOF\n{new_file_contents}")

    while True:
        res = input("Y/n - Would you like to add a model? ")
        if is_yes(res):
            while True:
                schema_singular = input("What is the singular label for this model? (ex. 'User') ")
                schema_plural = input("What is the plural label for this model? (ex. 'Users') " )
                res = input(f"Y/n - You selected {schema_singular} and {schema_plural} as the labels for this model. Is this correct? ")
                if is_yes(res):
                    break
            build_model(project_name, schema_singular, schema_plural)
            models.append( (schema_singular, schema_plural) )
        else:
            break
    return models

def build_controller(project_name, context_name):

    lines = [
       "using System;",
       "using System.Collections.Generic;",
       "using System.Diagnostics;",
       "using System.Linq;",
       "using System.Threading.Tasks;",
       "using Microsoft.AspNetCore.Mvc;",
       "using Microsoft.EntityFrameworkCore;",
       "using Microsoft.AspNetCore.Http; // for session",
       "using Microsoft.AspNetCore.Identity; // for password hashing", 
       f"using {project_name}.Models;",
       "",
       f"namespace {project_name}.Controllers",
       "{",
       "    public class HomeController : Controller",
       "    {",
       "",
       f"        private {context_name} dbContext;",
       "",
       f"        public HomeController({context_name} context)",
       "        {",
       "            dbContext = context;",
       "        }",
       "",
       "        // Base route",
       "        [HttpGet(\"\")]",
       "        public IActionResult Index()",
       "        {",
       "            return View();",
       "        }",
       "",
       "        public IActionResult Privacy()",
       "        {",
       "            return View();",
       "        }",
       "",
       "        [ResponseCache(Duration = 0, Location = ResponseCacheLocation.None, NoStore = true)]",
       "        public IActionResult Error()",
       "        {",
       "            return View(new ErrorViewModel { RequestId = Activity.Current?.Id ?? HttpContext.TraceIdentifier });",
       "        }",
       "    }",
       "}",
       "",
    ]

    new_file_contents = ""
    for line in lines:
        new_file_contents += line + "\n"
    os.system(f"cat > ./{project_name}/Controllers/HomeController.cs << EOF\n{new_file_contents}")

def build_layout(project_name):

    lines = [
       "<!DOCTYPE html>",
       "<html>",
       "<head>",
       "    <meta charset=\"utf-8\" />",
       "    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\" />",
       "    <title>@ViewData[\"Title\"] - TestProject</title>",
       "",
       "    <environment include=\"Development\">",
       "        <link rel=\"stylesheet\" href=\"~/lib/bootstrap/dist/css/bootstrap.css\" />",
       "    </environment>",
       "    <environment exclude=\"Development\">",
       "        <link rel=\"stylesheet\" href=\"https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css\"",
       "              asp-fallback-href=\"~/lib/bootstrap/dist/css/bootstrap.min.css\"",
       "              asp-fallback-test-class=\"sr-only\" asp-fallback-test-property=\"position\" asp-fallback-test-value=\"absolute\"",
       "              crossorigin=\"anonymous\"",
       "              integrity=\"sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T\"/>",
       "    </environment>",
       "    <link rel=\"stylesheet\" href=\"~/css/site.css\" />",
       "</head>",
       "<body>",
       "    <header>",
       "        <nav class=\"navbar navbar-expand-sm navbar-toggleable-sm navbar-light bg-white border-bottom box-shadow mb-3\">",
       "            <div class=\"container\">",
       "                <a class=\"navbar-brand\" asp-area=\"\" asp-controller=\"Home\" asp-action=\"Index\">TestProject</a>",
       "                <button class=\"navbar-toggler\" type=\"button\" data-toggle=\"collapse\" data-target=\".navbar-collapse\" aria-controls=\"navbarSupportedContent\"",
       "                        aria-expanded=\"false\" aria-label=\"Toggle navigation\">",
       "                    <span class=\"navbar-toggler-icon\"></span>",
       "                </button>",
       "                <div class=\"navbar-collapse collapse d-sm-inline-flex flex-sm-row-reverse\">",
       "                    <ul class=\"navbar-nav flex-grow-1\">",
       "                        <li class=\"nav-item\">",
       "                            <a class=\"nav-link text-dark\" asp-area=\"\" asp-controller=\"Home\" asp-action=\"Index\">Home</a>",
       "                        </li>",
       "                    </ul>",
       "                </div>",
       "            </div>",
       "        </nav>",
       "    </header>",
       "    <div class=\"container\">",
       "        <main role=\"main\" class=\"pb-3\">",
       "            @RenderBody()",
       "        </main>",
       "    </div>",
       "",
       "    <footer class=\"border-top footer text-muted\">",
       "        <div class=\"container\">",
       "            &copy; 2020 - TestProject - <a asp-area=\"\" asp-controller=\"Home\" asp-action=\"Privacy\">Privacy</a>",
       "        </div>",
       "    </footer>",
       "",
       "    <environment include=\"Development\">",
       "        <script src=\"~/lib/jquery/dist/jquery.js\"></script>",
       "        <script src=\"~/lib/bootstrap/dist/js/bootstrap.bundle.js\"></script>",
       "    </environment>",
       "    <environment exclude=\"Development\">",
       "        <script src=\"https://cdnjs.cloudflare.com/ajax/libs/jquery/3.3.1/jquery.min.js\"",
       "                asp-fallback-src=\"~/lib/jquery/dist/jquery.min.js\"",
       "                asp-fallback-test=\"window.jQuery\"",
       "                crossorigin=\"anonymous\"",
       "                integrity=\"sha256-FgpCb/KJQlLNfOu91ta32o/NMZxltwRo8QtmkMRdAu8=\">",
       "        </script>",
       "        <script src=\"https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.bundle.min.js\"",
       "                asp-fallback-src=\"~/lib/bootstrap/dist/js/bootstrap.bundle.min.js\"",
       "                asp-fallback-test=\"window.jQuery && window.jQuery.fn && window.jQuery.fn.modal\"",
       "                crossorigin=\"anonymous\"",
       "                integrity=\"sha384-xrRywqdh3PHs8keKZN+8zzc5TX0GRTLCcmivcbNJWm2rs5C8PRhcEn3czEjhAO9o\">",
       "        </script>",
       "    </environment>",
       "    <script src=\"~/js/site.js\" asp-append-version=\"true\"></script>",
       "",
       "    @RenderSection(\"Scripts\", required: false)",
       "</body>",
       "</html>",
       "",
    ]

    new_file_contents = ""
    for line in lines:
        new_file_contents += line + "\n"
    os.system(f"cat > ./{project_name}/Views/Shared/_Layout.cshtml << EOF\n{new_file_contents}")

def build_index(project_name):
    lines = [
       "@{",
       "    ViewData[\"Title\"] = \"Home Page\";",
       "}",
       "",
       "<div class=\"row\">",
       "    <div class=\"col-12 text-center\">",
       "        <h1>Launched with Viper</h1>",
       "    </div>",
       "</div",
    ]

    new_file_contents = ""
    for line in lines:
        new_file_contents += line + "\n"
    os.system(f"cat > ./{project_name}/Views/Home/Index.cshtml << EOF\n{new_file_contents}")

def add_login_and_registration(project_name, context_name):
    def build_user_class(project_name):
        lines = [
        "using System;",
        "using System.ComponentModel.DataAnnotations;",
        "using System.ComponentModel.DataAnnotations.Schema;",
        "",
        f"namespace {project_name}.Models",
        "{",
        "    public class User",
        "    {",
        "        [Key]",
        "        public int UserId { get; set; }",
        "",
        "        [Required]",
        "        [Display(Name = \"First Name\")]",
        "        public string FirstName { get; set; }",
        "",
        "        [Required]",
        "        [Display(Name = \"Last Name\")]",
        "        public string LastName { get; set; }",
        "",
        "        [EmailAddress]",
        "        [Required]",
        "        public string Email { get; set; }",
        "",
        "        [DataType(DataType.Password)]",
        "        [Required]",
        "        [MinLength(8, ErrorMessage = \"Password must be 8 characters or longer!\")]",
        "        public string Password { get; set; }",
        "",
        "        public DateTime CreatedAt { get; set; } = DateTime.Now;",
        "",
        "        public DateTime UpdatedAt { get; set; } = DateTime.Now;",
        "",
        "        // Will not be mapped to your users table!",
        "        [NotMapped]",
        "        [Compare(\"Password\")]",
        "        [DataType(DataType.Password)]",
        "        public string Confirm { get; set; }",
        "    }",
        "}",
        "",
        ]

        new_file_contents = ""
        for line in lines:
            new_file_contents += line + "\n"
        os.system(f"cat > ./{project_name}/Models/User.cs << EOF\n{new_file_contents}")

    def build_login_user_class(project_name):
        lines = [
        "using System;",
        "using System.ComponentModel.DataAnnotations;",
        "",
        f"namespace {project_name}.Models",
        "{",
        "    public class LoginUser",
        "    {",
        "        [Required]",
        "        [EmailAddress]",
        "        [Display(Name = \"Email\")]",
        "        public string LoginEmail { get; set; }",
        "",
        "        [Required]",
        "        [DataType(DataType.Password)]",
        "        [Display(Name = \"Password\")]",
        "        public string LoginPassword { get; set; }",
        "    }",
        "}",
        "",
        ]

        new_file_contents = ""
        for line in lines:
            new_file_contents += line + "\n"
        os.system(f"cat > ./{project_name}/Models/LoginUser.cs << EOF\n{new_file_contents}")

    def build_registration_partial():
        lines = [
        "",
        "@model User",
        "",
        "<form asp-action=\"Create\" method=\"post\">",
        "    <div class=\"form-group\">",
        "        <label asp-for=\"FirstName\"></label>&nbsp<span asp-validation-for=\"FirstName\" class=\"error-message\"></span>",
        "        <input asp-for=\"FirstName\" class=\"form-control\"/>",
        "    </div>",
        "    <div class=\"form-group\">",
        "        <label asp-for=\"LastName\"></label>&nbsp<span asp-validation-for=\"LastName\" class=\"error-message\"></span>",
        "        <input asp-for=\"LastName\" class=\"form-control\"/>",
        "    </div>",
        "    <div class=\"form-group\">",
        "        <label asp-for=\"Email\"></label>&nbsp<span asp-validation-for=\"Email\" class=\"error-message\"></span>",
        "        <input asp-for=\"Email\" class=\"form-control\"/>",
        "    </div>",
        "    <div class=\"form-group\">",
        "        <label asp-for=\"Password\"></label>&nbsp<span asp-validation-for=\"Password\" class=\"error-message\"></span>",
        "        <input asp-for=\"Password\" class=\"form-control\"/>",
        "    </div>",
        "    <div class=\"form-group\">",
        "        <label asp-for=\"Confirm\"></label>&nbsp<span asp-validation-for=\"Confirm\" class=\"error-message\"></span>",
        "        <input asp-for=\"Confirm\" class=\"form-control\"/>",
        "    </div>",
        "    <div class=\"form-group text-left\">",
        "        <button class=\"btn btn-primary\">Register</button>",
        "    </div>",
        "",
        "</form>",
        ]

        new_file_contents = ""
        for line in lines:
            new_file_contents += line + "\n"
        os.system(f"cat > ./{project_name}/Views/Home/RegistrationPartial.cshtml << EOF\n{new_file_contents}")

    def build_login_partial():
        lines = [
        "",
        "@model LoginUser",
        "",
        "<form asp-action=\"Login\" method=\"post\">",
        "",
        "    <div class=\"form-group\">",
        "        <label asp-for=\"LoginEmail\"></label>&nbsp<span asp-validation-for=\"LoginEmail\" class=\"error-message\"></span>",
        "        <input asp-for=\"LoginEmail\" class=\"form-control\" />",
        "    </div>",
        "",
        "    <div class=\"form-group\">",
        "        <label asp-for=\"LoginPassword\"></label>&nbsp<span asp-validation-for=\"LoginPassword\" class=\"error-message\"></span>",
        "        <input asp-for=\"LoginPassword\" class=\"form-control\" />",
        "    </div>",
        "    <div class=\"form-group text-right\">",
        "        <button class=\"btn btn-success\">Login</button>",
        "    </div>",
        "",
        "</form>",
        ]

        new_file_contents = ""
        for line in lines:
            new_file_contents += line + "\n"
        os.system(f"cat > ./{project_name}/Views/Home/LoginPartial.cshtml << EOF\n{new_file_contents}")

    def build_login_and_registration_index():
        lines = [
        "@{",
        "    ViewData[\"Title\"] = \"Home Page\";",
        "}",
        "",
        "<div class=\"row\">",
        "    <div class=\"col-12 text-center\">",
        "        <h1>Launched With Viper CLI</h1>",
        "        <h4>Login and Registration Partials</h4>",
        "    </div>",
        "</div>",
        "",
        "<div class=\"row\">",
        "    <div class=\"col-12 col-md-6\">",
        "        <partial name=\"RegistrationPartial\"></partial>",
        "    </div>",
        "    <div class=\"col-12 col-md-6\">",
        "        <partial name=\"LoginPartial\"></partial>",
        "    </div>",
        "</div>",
        ]

        new_file_contents = ""
        for line in lines:
            new_file_contents += line + "\n"
        os.system(f"cat > ./{project_name}/Views/Home/Index.cshtml << EOF\n{new_file_contents}")

    def build_controller_with_login_and_registration(project_name, context_name):

        lines = [
        "using System;",
        "using System.Collections.Generic;",
        "using System.Diagnostics;",
        "using System.Linq;",
        "using System.Threading.Tasks;",
        "using Microsoft.AspNetCore.Mvc;",
        "using Microsoft.EntityFrameworkCore;",
        "using Microsoft.AspNetCore.Http; // for session",
        "using Microsoft.AspNetCore.Identity; // for password hashing", 
        f"using {project_name}.Models;",
        "",
        f"namespace {project_name}.Controllers",
        "{",
        "    public class HomeController : Controller",
        "    {",
        "",
        f"        private {context_name} dbContext;",
        "",
        f"        public HomeController({context_name} context)",
        "        {",
        "            dbContext = context;",
        "        }",
        "",
        "        // ROUTE:               METHOD:                VIEW:",
        "        // -----------------------------------------------------------------------------------",
        "        // GET(\"\")              Index()                Index.cshtml",
        "        // POST(\"/register\")    Create(User user)      ------ (Index.cshtml to display errors)",
        "        // POST(\"/login\")       Login(LoginUser user)  ------ (Index.cshtml to display errors)",
        "        // GET(\"/logout\")       Logout()               ------",
        "        // GET(\"/success\")      Success()              Success.cshtml",
        "",
        "        [HttpGet(\"\")]",
        "        public IActionResult Index()",
        "        {",
        "            //List<User> AllUsers = dbContext.Users.ToList();",
        "            return View();",
        "        }",
        "",
        "        [HttpPost(\"/register\")]",
        "        public IActionResult Create(User user)",
        "        {",
        "            if (ModelState.IsValid)",
        "            {",
        "                // If a User exists with provided email",
        "                if (dbContext.Users.Any(u => u.Email == user.Email))",
        "                {",
        "                    // Manually add a ModelState error to the Email field",
        "                    ModelState.AddModelError(\"Email\", \"Email already in use!\");",
        "                    return View(\"Index\");",
        "                }",
        "",
        "                // hash password",
        "                PasswordHasher<User> Hasher = new PasswordHasher<User>();",
        "                user.Password = Hasher.HashPassword(user, user.Password);",
        "",
        "                // create user",
        "                dbContext.Add(user);",
        "                dbContext.SaveChanges();",
        "",
        "                // sign user into session",
        "                var NewUser = dbContext.Users.FirstOrDefault(u => u.Email == user.Email);",
        "                int UserId = NewUser.UserId;",
        "                HttpContext.Session.SetInt32(\"UserId\", UserId);",
        "",
        "                // go to success",
        "                return RedirectToAction(\"Success\");",
        "            }",
        "            // display errors",
        "            else",
        "            {",
        "                return View(\"Index\");",
        "            }",
        "        }",
        "",
        "        [HttpPost(\"/login\")]",
        "        public IActionResult Login(LoginUser user)",
        "        {",
        "            if (ModelState.IsValid)",
        "            {",
        "                var userInDb = dbContext.Users.FirstOrDefault(u => u.Email == user.LoginEmail);",
        "                if (userInDb == null)",
        "                {",
        "                    // Add an error to ModelState and return to View!",
        "                    ModelState.AddModelError(\"LoginEmail\", \"Invalid Email/Password\");",
        "                    return View(\"Index\");",
        "                }",
        "                // Initialize hasher object",
        "                var hasher = new PasswordHasher<LoginUser>();",
        "",
        "                // verify provided password against hash stored in db",
        "                var result = hasher.VerifyHashedPassword(user, userInDb.Password, user.LoginPassword);",
        "                if (result == 0)",
        "                {",
        "                    // handle failure (this should be similar to how \"existing email\" is handled)",
        "                    ModelState.AddModelError(\"LoginPassword\", \"Password is invalid.\");",
        "                    return View(\"Index\");",
        "                }",
        "",
        "                // sign user into session",
        "                int UserId = userInDb.UserId;",
        "                HttpContext.Session.SetInt32(\"UserId\", UserId);",
        "",
        "                return RedirectToAction(\"Success\");",
        "            }",
        "            // display errors",
        "            else",
        "            {",
        "                return View(\"Index\");",
        "            }",
        "        }",
        "",
        "        [HttpGet(\"/logout\")]",
        "        public IActionResult Logout()",
        "        {",
        "            HttpContext.Session.Clear();",
        "            return RedirectToAction(\"Index\");",
        "        }",
        "",
        "        [HttpGet(\"success\")]",
        "        public IActionResult Success()",
        "        {",
        "            int? userId = HttpContext.Session.GetInt32(\"UserId\");",
        "            if (userId == null)",
        "            {",
        "                return RedirectToAction(\"Index\");",
        "            }",
        "            return View();",
        "        }",
        "",
        "        public IActionResult Privacy()",
        "        {",
        "            return View();",
        "        }",
        "",
        "        [ResponseCache(Duration = 0, Location = ResponseCacheLocation.None, NoStore = true)]",
        "        public IActionResult Error()",
        "        {",
        "            return View(new ErrorViewModel { RequestId = Activity.Current?.Id ?? HttpContext.TraceIdentifier });",
        "        }",
        "    }",
        "}",
        "",
        ]

        new_file_contents = ""
        for line in lines:
            new_file_contents += line + "\n"
        os.system(f"cat > ./{project_name}/Controllers/HomeController.cs << EOF\n{new_file_contents}")

    def customize_css(project_name):
        lines = [
        ".error-message{",
        "    font-size: 14px;",
        "    color: red;",
        "}",
        ]
        new_file_contents = ""
        for line in lines:
            new_file_contents += line + "\n"
        os.system(f"cat >> ./{project_name}/wwwroot/css/site.css << EOF\n{new_file_contents}")

    build_user_class(project_name)
    build_login_user_class(project_name)
    build_registration_partial()
    build_login_partial()
    build_login_and_registration_index()
    build_controller_with_login_and_registration(project_name, context_name)
    customize_css(project_name)

def viper():
    print("Welcome to Viper. Let's build a project.")
    project_name = input("Enter project name: ")

    MySql_Database = input("Which MySql Database are you using? ")
    MySql_Username = input("Enter your MySql username: ")
    MySql_Password = input("Enter your MySql password: ")

    global_json() # Create global.json file to specifiy using sdk 2.2.107
    os.system(f"dotnet new mvc --no-https -o {project_name}")
    os.system(f"dotnet add ./{project_name} package Pomelo.EntityFrameworkCore.MySql -v 2.2.0")

    models = []
    context = input("Enter name of context: ")
    use_login_and_registration = input("Y/n - Would you like to add Login and Registration? ")
    if use_login_and_registration in ["Y","y","YES","Yes","yes"]:
        use_login_and_registration = True
    else:
        use_login_and_registration = False
    if use_login_and_registration:
        models.append( ("User", "Users") )
        # run login_and_reg codes
        add_login_and_registration(project_name, context)

    models += build_models(project_name)

    # context = input("Enter name of context: ")
    build_context_file(project_name, context, models)
    build_startup_file(project_name, context)
    if not use_login_and_registration:
        build_controller(project_name, context)
    build_layout(project_name)
    if not use_login_and_registration:
        build_index(project_name)

    os.system(f"git -C {project_name} init") # run git init
    appsettings_json(project_name, MySql_Database, MySql_Username, MySql_Password) # add appsettings.json with DBInfo
    gitignore(project_name) # Add .gitignore

    path = f"{pathlib.Path(__file__).parent.absolute()}/{project_name}"
    os.system(f"dotnet watch -p {path} run")

    return True

if __name__ == "__main__":
    viper()

