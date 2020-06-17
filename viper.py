import os
import pathlib
import fileinput
import sys

def candy():
    header = [
        "      _    _ _____  _____  _______  ______      _______        _____",
        "       \  /    |   |_____] |______ |_____/      |       |        |  ",
        "        \/   __|__ |       |______ |    \_      |_____  |_____ __|__",
    ]
    aspnet = [
        "            ____ ____ ___   _  _ ____ ___    ____ ____ ____ ____ ",
        "            |__| [__  |__]  |\ | |___  |     |    |  | |__/ |___ ",
        "            |  | ___] |    .| \| |___  |     |___ |__| |  \ |___ ",
    ]
    header_string = "".join([s + "\n" for s in header])
    aspnet_string = "".join([s + "\n" for s in aspnet])

    footer = [
        "_   _ ____ _  _ . ____ ____    ____ _    _       ____ ____ ___",
        " \_/  |  | |  | ' |__/ |___    |__| |    |       [__  |___  | ",  
        "  |   |__| |__|   |  \ |___    |  | |___ |___    ___] |___  | ",
        "       ____ ____ ___    ____ ____ ___ ____ ____    _ ___      ",              
        "       | __ |___  |     |__| |___  |  |___ |__/    |  |       ",        
        "       |__] |___  |     |  | |     |  |___ |  \    |  |       ",      
    ]
    footer_string = "".join([s + "\n" for s in footer])
    candies = [header_string,aspnet_string,footer_string]
    return candies

def appsettings_json(project_name, database, username, password):
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
    os.system(f"touch ./{project_name}/.gitignore")
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

def build_models(project_name, context_name):

    models = []
    controller_lines = []
    layout_lines = []

    def is_yes(res):
        return res in ["y", "Y", "yes", "Yes", "YES"]

    def build_model(project_name, schema_singular, schema_plural, context_name):

        attributes = []
        
        lines1 = [
        "using System;",
        "using System.Collections.Generic;",
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
            res = input(f'\033[92m{"Y/n - Would you like to add an attribute? "}\033[00m')
            if is_yes(res):
                label = input(f'\033[92m{"What is this attribute called? "}\033[00m')
                attributes.append(label)
                stype = input(f'\033[92m{"What is this attributes type? "}\033[00m')
                required = input(f'\033[92m{"Y/n - Is this attribute required? "}\033[00m')
                display = ""
                while True:
                    change_display = input(f'\033[92m{"Y/n - Would you like to change the default display? "}\033[00m')
                    if is_yes(change_display):
                        d = input(f'\033[92m{"Enter custom display message: "}\033[00m')
                        message = f"Y/n - You wrote -- {d} -- as your custom display message. Is this correct? "
                        r = input(f'\033[92m{message}\033[00m')
                        if is_yes(r):
                            display = d
                            break
                    else:
                        break

                validations = []
                while True:
                    res = input(f'\033[92m{"Y/n - Would you like to add a validation to this attribute? "}\033[00m')
                    if is_yes(res):
                        validation = input(f'\033[92m{"Please enter your validation exactly as it would appear in C#. For example: [Range(1,5)] "}\033[00m')
                        message = f"Y/n - You entered: {validation} as your validation. Is this correct? "
                        r = input(f'\033[92m{message}\033[00m')
                        if is_yes(r):
                            validations.append(validation)
                    else:
                        break
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
        "        // One-To-Many (One-side) nav property goes here <<\n",
        "        // One-To-Many (Many-side) nav property goes here <<\n",
        "",
        "        // Many-To-Many nav property goes here <<",
        "",
        "        [Required]",
        "        public DateTime CreatedAt { get; set; } = DateTime.Now;",
        "",
        "        [Required]",
        "        public DateTime UpdatedAt { get; set; } = DateTime.Now;",
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

        wants_crud = input(f'\033[92m{"Y/n - Do you want Viper to build out basic CRUD functionality for this model? "}\033[00m')
        
        controller_lines = []
        layout_lines = []

        if is_yes(wants_crud):
            controller_lines, layout_lines = CRUD(project_name, schema_singular, schema_plural, attributes, context_name)

        return controller_lines, layout_lines

    while True:
        res = input(f'\033[92m{"Y/n - Would you like to add a model? "}\033[00m')
        if is_yes(res):
            while True:
                schema_singular = input(f'\033[92m{"What is the singular label for this model? (ex. User) "}\033[00m')
                schema_plural = input(f'\033[92m{"What is the plural label for this model? (ex. Users) "}\033[00m')
                message = f"Y/n - You selected {schema_singular} and {schema_plural} as the labels for this model. Is this correct? "
                res = input(f'\033[92m{message}\033[00m')
                if is_yes(res):
                    break
            new_controller_lines, new_layout_lines = build_model(project_name, schema_singular, schema_plural, context_name)
            controller_lines += new_controller_lines
            layout_lines += new_layout_lines
            models.append( (schema_singular, schema_plural) )
        else:
            break
    return [models, controller_lines, layout_lines]

def build_controller(project_name, context_name, extra_lines=[]):

    lines1 = [
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
    ]
    lines2 = [
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
    lines = lines1 + extra_lines + lines2
    new_file_contents = ""
    for line in lines:
        new_file_contents += line + "\n"
    os.system(f"cat > ./{project_name}/Controllers/HomeController.cs << EOF\n{new_file_contents}")

def build_layout(project_name, extra_lines, session=False):

    lines0 = []
    if session:
        lines0.append("@using Microsoft.AspNetCore.Http")

    lines1 = [
       "<!DOCTYPE html>",
       "<html>",
       "<head>",
       "    <meta charset=\"utf-8\" />",
       "    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\" />",
       f"    <title>@ViewData[\"Title\"] - {project_name}</title>",
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
       f"                <a class=\"navbar-brand\" asp-area=\"\" asp-controller=\"Home\" asp-action=\"Index\">{project_name}</a>",
       "                <button class=\"navbar-toggler\" type=\"button\" data-toggle=\"collapse\" data-target=\".navbar-collapse\" aria-controls=\"navbarSupportedContent\"",
       "                        aria-expanded=\"false\" aria-label=\"Toggle navigation\">",
       "                    <span class=\"navbar-toggler-icon\"></span>",
       "                </button>",
       "                <div class=\"navbar-collapse collapse d-sm-inline-flex flex-sm-row-reverse\">",
       "                    <ul class=\"navbar-nav flex-grow-1\">",
       "                        <li class=\"nav-item\">",
       "                            <a class=\"nav-link text-dark\" asp-area=\"\" asp-controller=\"Home\" asp-action=\"Index\">Home</a>",
       "                        </li>",
    ]


    lines2 = [
       "                    </ul>",
       "                </div>",
    ]
    if session:
        lines2.append('                @if (Context.Session.GetInt32("UserId") != null)')
        lines2.append('                {')
        lines2.append('                    <a asp-action="Logout">Logout</a>')
        lines2.append('                }')

    lines3 = [
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

    lines = lines0 + lines1 + extra_lines + lines2 + lines3
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

def CRUD(project_name, schema_s, schema_p, attributes, context_name):

    # Create View Directory
    os.system(f"mkdir ./{project_name}/Views/{schema_s}")

    # Build Controller
    def build_controller(project_name, schema_s, schema_p, context_name):
        s = schema_s
        p = schema_p
        controller =  [
            "using System;",
            "using System.Collections.Generic;",
            "using System.Diagnostics;",
            "using System.Linq;",
            "using System.Threading.Tasks;",
            "using Microsoft.AspNetCore.Mvc;",
            "using Microsoft.EntityFrameworkCore;",
            "using Microsoft.AspNetCore.Http;",
            "using Microsoft.AspNetCore.Identity;",
            f"using {project_name}.Models;",
            "",
            f"namespace {project_name}.Controllers",
            "{",
            f"    public class {s}Controller : Controller",
            "    {",
            f"        private {context_name} dbContext;",
            "",
            f"        public {s}Controller({context_name} context) " + "{ dbContext = context; }",
            "",
            f"        ///////////// BEGINNING OF CRUD METHODS FOR {s.upper()} MODEL /////////////",
            "",
            "        //    REQUEST:      ROUTE:                     METHOD:",
            "        //    --------------------------------------------------------------",
            f"        //    GET           /{p.lower()}                     {p}()",
            f"        //    GET/POST      /{s.lower()}/create               GET-> Create{s}Form() / POST -> Create{s}({s} {s.lower()})",
            f"        //    GET           /{s.lower()}/"+"{"+f"{s}Id"+"}"+f"             {s}(int {s.lower()}Id)",
            f"        //    GET/POST      /{s.lower()}/"+"{"+f"{s.lower()}Id"+"}"+f"/update      GET-> Edit{s}(int {s.lower()}Id) / POST-> Update{s}(int {s.lower()}Id, {s} {s.lower()})",
            f"        //    POST          /{s.lower()}/"+"{"+f"{s.lower()}Id"+"}"+f"/delete      Delete{s}(int {s.lower()}Id)",
            "",
            "        // Helper Functions",
            f"        public {s}[] GetAll{p}() "+"{"+f" return dbContext.{p}.ToArray(); "+"}",
            f"        public {s} GetOneSingle{s}ById (int {s.lower()}Id) "+"{"+f" return dbContext.{p}.FirstOrDefault({p.lower()[0]} => {p.lower()[0]}.{s}Id == {s.lower()}Id); "+"}",
            f"        public IActionResult GetCreate{s}Form () "+"{"+f" ViewBag.Message = \"Add\"; ViewBag.{s}Id = \"\"; return View(\"CreateOrUpdate{s}\"); "+"}",
            f"        public IActionResult GetEdit{s}Form(int {s.lower()}Id) "+"{"+f" ViewBag.Message = \"Edit\"; ViewBag.{s}Id = {s.lower()}Id; return View(\"CreateOrUpdate{s}\", GetOneSingle{s}ById({s.lower()}Id)); "+"}",
            "",
            f"        [HttpGet(\"{p.lower()}\")]",
            f"        public IActionResult {p}() "+"{"+f" return View(\"{p}\", GetAll{p}()); "+"}",
            "",
            f"        [HttpGet(\"{s.lower()}/create\")]",
            f"        public IActionResult Create{s}Form() "+"{"+f" return GetCreate{s}Form(); "+"}",
            "",
            f"        [HttpPost(\"{s.lower()}/create\")]",
            f"        public IActionResult Create{s}({s} {s.lower()})",
            "        {",
            "            if (ModelState.IsValid)",
            "            {",
            f"                dbContext.Add({s.lower()});",
            "                dbContext.SaveChanges();",
            f"                return RedirectToAction(\"{p}\");",
            "            }",
            f"            return GetCreate{s}Form();",
            "        }",
            "",
            f"        [HttpGet(\"{s.lower()}/"+"{"+f"{s.lower()}Id"+"}\")]",
            f"        public IActionResult {s}(int {s.lower()}Id) "+"{"+f" return View(\"{s}\", GetOneSingle{s}ById({s.lower()}Id)); "+"}",
            "",
            f"        [HttpGet(\"{s.lower()}/"+"{"+f"{s.lower()}Id"+"}/update\")]",
            f"        public IActionResult Edit{s}(int {s.lower()}Id) "+"{"+f" return GetEdit{s}Form({s.lower()}Id); "+"}",
            "",
            f"        [HttpPost(\"{s.lower()}/"+"{"+f"{s.lower()}Id"+"}/update\")]",
            f"        public IActionResult Update{s}(int {s.lower()}Id, {s} {s.lower()})",
            "        {",
            "            if (ModelState.IsValid)",
            "            {",
            f"                dbContext.Update({s.lower()});",
            f"                dbContext.Entry({s.lower()}).Property(\"CreatedAt\").IsModified = false;",
            "                dbContext.SaveChanges();",
            f"                return RedirectToAction(\"{s}\", {s.lower()});",
            "            }",
            "            else { return "+f"GetEdit{s}Form({s.lower()}Id); "+"}",
            "        }",
            "",
            f"        [HttpPost(\"{s.lower()}/"+"{"+f"{s.lower()}Id"+"}/delete\")]",
            f"        public IActionResult Delete{s}(int {s.lower()}Id)",
            "        {",
            f"            dbContext.{p}.Remove(GetOneSingle{s}ById({s.lower()}Id));",
            "            dbContext.SaveChanges();",
            f"            return RedirectToAction(\"{p}\");",
            "        }",
            "",
            f"        ///////////// END OF CRUD METHODS FOR {s.upper()} MODEL /////////////",
            "",
            "        [ResponseCache(Duration = 0, Location = ResponseCacheLocation.None, NoStore = true)]",
            "        public IActionResult Error()",
            "        {",
            "            return View(new ErrorViewModel { RequestId = Activity.Current?.Id ?? HttpContext.TraceIdentifier });",
            "        }",
            "    }",
            "}",
            "",
            "",
        ]

        new_file_contents = ""
        for line in controller:
            new_file_contents += line + "\n"

        os.system(f"cat > ./{project_name}/Controllers/{schema_s}Controller.cs << EOF\n{new_file_contents}")

    # Build schema_s view
    def build_schema_s_view(project_name, schema_s, schema_p, attributes):
        s = schema_s
        p = schema_p
        lines1 = [
            "@{",
            f"    ViewData[\"Title\"] = \"{s}\";",
            "}",
            "",
            f"@model {s}",
            "@{ string UpdateUrl = $\"/"+f"{s.lower()}"+"/{@Model."+f"{s}"+"Id}/update\"; }",
            "",
            "<div class=\"row\">",
            "    <div class=\"col-12 text-center\">",
            f"        <h1>Read / Update / Delete a {s}</h1>",
            "    </div>",
            "</div>",
            "",
            "<div class=\"row\">",
            "    <div class=\"col-12 text-center\">",
            f"        <p>Id: @Model.{s}Id</p>",
        ]
 
        lines2 = []
        for attribute in attributes:
            lines2.append(f"        <p>{attribute}: @Model.{attribute}</p>")
 
        lines3 = [
            "    </div>",
            "</div>",
            "",
            "<div class=\"row\">",
            "    <div class=\"col-12 col-md-10 offset-md-1\">",
            f"        <form asp-action=\"Delete{s}\" asp-route-{s.lower()}Id=@Model.{s}Id asp-controller=\"{s}\" method=\"post\">",
            "            <input type=\"hidden\" name=\"Delete\" />",
            "            <div class=\"form-group text-center\"> ",
            f"                <a href=@UpdateUrl class=\"btn btn-info\">Edit this {s}</a>",
            f"                <button class=\"btn btn-danger\">Delete this {s}</button>",
            "            </div>",
            "        </form>",
            "    </div>",
            "</div>",
            "",
            "",
        ]

        lines = lines1 + lines2 + lines3
        new_file_contents = ""
        for line in lines:
            new_file_contents += line + "\n"

        os.system(f"cat > ./{project_name}/Views/{s}/{schema_s}.cshtml << EOF\n{new_file_contents}")

    # Build schema_p view
    def build_schema_p_view(project_name, schema_s, schema_p, attributes):
        s = schema_s
        p = schema_p
        lines1 = [
            "@{",
            f"    ViewData[\"Title\"] = \"All {p}\";",
            "}",
            "",
            f"@model {s}[]",
            "",
            "<div class=\"row\">",
            "    <div class=\"col-12 text-center\">",
            f"        <h1>All {p}</h1>",
            "    </div>",
            "</div>",
            "",
            "<div class=\"row\">",
            "    <div class=\"col-12 col-md-10 offset-md-1\">",
            "        <table class=\"table table-bordered table-striped\">",
            "            <thead class=\"thead-dark\">",
            "                <tr>",
            "                    <th>Id</th>",
        ]
        
        lines2 = []
        for attribute in attributes:
            lines2.append(f"                    <th>{attribute}</th>")
        
        lines3 = [
            "                    <th>Created At</th>",
            "                    <th>Updated At</th>",
            "                </tr>",
            "            </thead>",
            "            <tbody>",
            f"                @foreach ({s} {s.lower()} in Model)",
            "                {",
            f"                    string url = $\"/{s.lower()}/"+"{"+f"{s.lower()}.{s}Id"+"}\";",
            "                <tr>",
            f"                    <td>@{s.lower()}.{s}Id</td>",
        ]
        
        lines4 = []
        lines4.append(f"                    <td><a href=@url>@{s.lower()}.{attributes[0]}</a></td>")
        for attribute in attributes[1::]:
            lines4.append(f"                    <td>@{s.lower()}.{attribute}</td>")
        
        lines5 = [
            f"                    <td>@{s.lower()}.CreatedAt</td>",
            f"                    <td>@{s.lower()}.UpdatedAt</td>",
            "                </tr>",
            "                }",
            "            </tbody>",
            "        </table>",
            "    </div>",
            "</div>",
            "",
            "<div class=\"row\">",
            "    <div class=\"col-12 col-md-10 offset-md-1 text-right\">",
            f"        <a href=\"{s.lower()}/create\" class=\"btn btn-primary\">Create a {s}</a>",
            "    </div>",
            "</div>",
            "",
            "",
        ]
        lines = lines1 + lines2 + lines3 + lines4 + lines5
        new_file_contents = ""
        for line in lines:
            new_file_contents += line + "\n"

        os.system(f"cat > ./{project_name}/Views/{s}/{schema_p}.cshtml << EOF\n{new_file_contents}")

    # Build create/update form
    def build_create_or_edit_view(project_name, schema_s, schema_p, attributes):
        s = schema_s
        p = schema_p
        lines1 = [
            "@{",
            f"    ViewData[\"Title\"] = \"Create/Edit a {s}\";",
            "}",
            "",
            f"@model {s}",
            "",
            "",
            "<div class=\"row\">",
            "    <div class=\"col-12 text-center\">",
            f"        <h1>@ViewBag.Message a {s}</h1>",
            "    </div>",
            "</div>",
            "",
            "@if (ViewBag.Message == \"Edit\")",
            "{",
            "    <div class=\"row\">",
            "        <div class=\"col-12 col-md-10 offset-md-1\">",
            f"            <form asp-action=\"Update{s}\" asp-controller=\"{s}\" method=\"post\" asp-route-{s.lower()}Id=\"@ViewBag.{s}Id\">",
            "",
        ]
        lines2 = []
        for attribute in attributes:
            lines2.append("            <div class=\"form-group\">")
            lines2.append(f"                <label asp-for=\"{attribute}\"></label>&nbsp<span asp-validation-for=\"{attribute}\" class=\"error-message\"></span>")
            lines2.append(f"                <input asp-for=\"{attribute}\" class=\"form-control\" />")
            lines2.append("            </div>")

        lines3 = [
            "                <div class=\"form-group text-right\">",
            f"                    <button class=\"btn btn-primary\">@ViewBag.Message a {s}</button>",
            "                </div>",
            "            </form>",
            "        </div>",
            "    </div>",
            "}",
            "",
            "else",
            "{",
            "    <div class=\"row\">",
            "        <div class=\"col-12 col-md-10 offset-md-1\">",
            f"            <form asp-action=\"Create{s}\" asp-controller=\"{s}\" method=\"post\">",
            "",
        ]
        lines4 = []
        for attribute in attributes:
            lines4.append("            <div class=\"form-group\">")
            lines4.append(f"                <label asp-for=\"{attribute}\"></label>&nbsp<span asp-validation-for=\"{attribute}\" class=\"error-message\"></span>")
            lines4.append(f"                <input asp-for=\"{attribute}\" class=\"form-control\" />")
            lines4.append("            </div>")

        lines5 = [
            "                <div class=\"form-group text-right\">",
            f"                    <button class=\"btn btn-primary\">@ViewBag.Message a {s}</button>",
            "                </div>",
            "            </form>",
            "        </div>",
            "    </div>",
            "}",
            "",
            "",
            "",
            "",
        ]
        lines = lines1 + lines2 + lines3 + lines4 + lines5

        new_file_contents = ""
        for line in lines:
            new_file_contents += line + "\n"

        os.system(f"cat > ./{project_name}/Views/{s}/CreateOrUpdate{schema_s}.cshtml << EOF\n{new_file_contents}")

    # Build layout navbar
    def build_layout_navbar_lines(project_name, schema_s, schema_p):
        lines = [
            "                        <li class=\"nav-item\">",
            f"                            <a class=\"nav-link text-dark\" asp-area=\"\" asp-controller=\"{schema_s}\" asp-action=\"{schema_p}\">{schema_p}</a>",
            "                        </li>",
        ]
        return lines

    build_controller(project_name, schema_s, schema_p, context_name)
    build_schema_s_view(project_name, schema_s, schema_p, attributes)
    build_schema_p_view(project_name, schema_s, schema_p, attributes)
    build_create_or_edit_view(project_name, schema_s, schema_p, attributes)

    return [], build_layout_navbar_lines(project_name, schema_s, schema_p)

def add_login_and_registration(project_name, context_name, extra_controller_lines):
    def is_yes(res):
        return res in ["y", "Y", "yes", "Yes", "YES"]
    
    def build_user_class(project_name):
        lines1 = [
            "using System;",
            "using System.Collections.Generic;",
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
        ]

        lines2 = []

        lines3 = [
            "        // One-To-Many (One-side) nav property goes here <<\n",
            "        // One-To-Many (Many-side) nav property goes here <<\n",
            "",
            "        // Many-To-Many nav property goes here <<",
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
        lines = lines1 + lines2 + lines3
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

    def build_controller_with_login_and_registration(project_name, context_name, extra_controller_lines):

        lines1 = [
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
        ]

        lines2 = [
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
        lines = lines1 + extra_controller_lines + lines2
        new_file_contents = ""
        for line in lines:
            new_file_contents += line + "\n"
        os.system(f"cat > ./{project_name}/Controllers/HomeController.cs << EOF\n{new_file_contents}")

    def build_success():
        lines =  [
        "@{",
        "    ViewData[\"Title\"] = \"Success\";",
        "}",
        "",
        "<div class=\"row\">",
        "    <div class=\"col-12 text-right\">",
        "        <a href=\"/logout\">Logout</a>",
        "    </div>",
        "</div>",
        "",
        "<div class=\"row\">",
        "    <div class=\"col-12 text-center\">",
        "        <h1 class=\"text-success\">Success</h1>",
        "    </div>",
        "</div>",
        "",
        ]
        new_file_contents = ""
        for line in lines:
            new_file_contents += line + "\n"

        os.system(f"cat > ./{project_name}/Views/Home/Success.cshtml << EOF\n{new_file_contents}")

    build_user_class(project_name)
    build_login_user_class(project_name)
    build_registration_partial()
    build_login_partial()
    build_login_and_registration_index()
    build_controller_with_login_and_registration(project_name, context_name, extra_controller_lines)
    # customize_css(project_name)
    build_success()

def map_database_relationships(project_name, models):

    display_models = [model[0] for model in models]

    def is_yes(res):
        return res.lower() in ["y", "yes"]    

    def create_joining_table(project_name, joining_table_name, model1, model2):
        lines = [
            "using System;",
            "using System.Collections.Generic;",
            "using System.ComponentModel.DataAnnotations;",
            "",
            f"namespace {project_name}.Models",
            "{",
            f"    public class {joining_table_name}",
            "    {",
            "        [Key]",
            f"        public int {joining_table_name}Id " +"{ get; set; }",
            "",
            f"        public int {model1}Id " + "{ get; set; }",
            f"        public int {model2}Id " + "{ get; set; }",
            f"        public {model1} {model1} " + "{ get; set; }",
            f"        public {model2} {model2} " + "{ get; set; }",
            "        [Required]",
            "        public DateTime CreatedAt { get; set; } = DateTime.Now;",
            "",
            "        [Required]",
            "        public DateTime UpdatedAt { get; set; } = DateTime.Now;",
            "    }",
            "}",
            "",
        ]
        new_file_contents = ""
        for line in lines:
            new_file_contents += line + "\n"

        os.system(f"touch ./{project_name}/Models/{joining_table_name}.cs")
        os.system(f"cat > ./{project_name}/Models/{joining_table_name}.cs << EOF\n{new_file_contents}")
    
    def add_many_to_many_relationship(project_name, model1, model2, m1_nav_property, m2_nav_property):
        search_exp = "        // Many-To-Many nav property goes here <<"

        file1 = f"./{project_name}/Models/{model1}.cs"
        file2 = f"./{project_name}/Models/{model2}.cs"
        
        # Update First Model
        for line in fileinput.input(file1, inplace=1):
            if search_exp in line:
                line = line.replace(search_exp, f"{m1_nav_property}{search_exp}")
            sys.stdout.write(line)

        # Update Second Model
        for line in fileinput.input(file2, inplace=1):
            if search_exp in line:
                line = line.replace(search_exp, f"{m2_nav_property}{search_exp}")
            sys.stdout.write(line)

    def add_one_to_many_relationship(project_name, one_model, many_model, model1_nav_property, model2_nav_property, model2_foreign_key):
        model1_search_exp = "        // One-To-Many (One-side) nav property goes here <<\n"
        model2_search_exp = "        // One-To-Many (Many-side) nav property goes here <<\n"

        file1 = f"./{project_name}/Models/{one_model}.cs"
        file2 = f"./{project_name}/Models/{many_model}.cs"

        # Update One Model
        for line in fileinput.input(file1, inplace=1):
            if model1_search_exp in line:
                line = line.replace(model1_search_exp, f"{model1_nav_property}{model1_search_exp}")
            sys.stdout.write(line)

        # Update Many Model
        for line in fileinput.input(file2, inplace=1):
            if model2_search_exp in line:
                line = line.replace(model2_search_exp, f"{model2_foreign_key}{model2_nav_property}{model2_search_exp}")
            sys.stdout.write(line)

    # one-to-many
    message = "Let's configure your database relationships."
    print(f'\033[92m{message}\033[00m')

    while True:
        wants_one_to_many = is_yes(input(f'\033[92m{"Y/n - Would you like to add a one-to-many relationship between two models? "}\033[00m'))
        if not wants_one_to_many:
            break
        error_message = "Oops, that model doesn't exist. "
        message = f"Your models include: {display_models}"
        print(f'\033[92m{message}\033[00m')
        model1 = ""
        model2 = ""
        while True:
            message = "Please enter the name of the model on the 'One' side of this relationship: "
            model1 = input(f'\033[92m{message}\033[00m')
            if model1 in display_models:
                break
            print(f'\033[92m{error_message}\033[00m')
        while True:
            message = "Please enter the name of the model on the 'Many' side of this relationship: "
            model2 = input(f'\033[92m{message}\033[00m')
            if model2 in display_models:
                break
            print(f'\033[92m{error_message}\033[00m')
        
        # add navigation property to One Model
        message = "What is the label of the 'One' model's navigation property? "
        m1_nav_prop_label = input(f'\033[92m{message}\033[00m')
        m1_nav_property = f"        public List<{model2}> {m1_nav_prop_label} " + "{ get; set; }\n"

        # add foreign key and navigation property to Many Model
        message = "What is the label of the 'Many' model's navigation property? "
        m2_nav_prop_label = input(f'\033[92m{message}\033[00m')
        m2_foreign_key = f"        public int {model1}Id " + "{ get; set; }\n"
        m2_nav_property = f"        public {model1} {m2_nav_prop_label} " + "{ get; set; }\n"

        message = f"Y/n - Add this relationship between {model1} and {model2}? "
        res = input(f'\033[92m{message}\033[00m')
        if not is_yes(res):
            break
        
        # update files:
        add_one_to_many_relationship(project_name, model1, model2, m1_nav_property, m2_nav_property, m2_foreign_key)
        
    # many-to-many
    while True:
        wants_many_to_many = is_yes(input(f'\033[92m{"Y/n - Would you like to add a many-to-many relationship between two models? "}\033[00m'))
        if not wants_many_to_many:
            break
        message = f"Your models include: {display_models}"
        print(f'\033[92m{message}\033[00m')
        model1 = ""
        model2 = ""
        while True:
            model1 = input(f'\033[92m{"Please enter the name of the first model: "}\033[00m')
            if model1 in display_models:
                break
            print(f'\033[92m{error_message}\033[00m')
        while True:
            model2 = input(f'\033[92m{"Please enter the name of the second model: "}\033[00m')
            if model2 in display_models:
                break
            print(f'\033[92m{error_message}\033[00m')
        
        message = f"What is the singular name of the joining table between {model1} and {model2}? "
        joining_table = input(f'\033[92m{message}\033[00m')

        message = f"What is the plural name of the joining table between {model1} and {model2}? "
        joining_table_plural = input(f'\033[92m{message}\033[00m')

        models.append( (joining_table, joining_table_plural ))

        message = f"What is the label of {model1}'s navigation property? "
        m1_nav_prop_label = input(f'\033[92m{message}\033[00m')
        m1_nav_property = f"        public List<{joining_table}> {m1_nav_prop_label} " + "{ get; set; }\n"

        message = f"What is the label of {model2}'s navigation property? "
        m2_nav_prop_label = input(f'\033[92m{message}\033[00m')
        m2_nav_property = f"        public List<{joining_table}> {m2_nav_prop_label} " + "{ get; set; }\n"

        create_joining_table(project_name, joining_table, model1, model2)
        add_many_to_many_relationship(project_name, model1, model2, m1_nav_property, m2_nav_property)

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

def make_migrations(project_name, message):
    migration_name = input(f'\033[92m{"What is this migration called (i.e., FirstMigration): "}\033[00m')
    os.chdir(f"{pathlib.Path(__file__).parent.absolute()}/{project_name}")
    os.system(f"dotnet ef migrations add {migration_name}")
    os.system(f"dotnet ef database update")
    print()
    print(f'\033[93m{message}\033[00m')
    print(f'\033[93m{"                Thanks for using Viper CLI."}\033[00m')
    print(f'\033[93m{"                  Launching your project..."}\033[00m')

    os.system(f"dotnet watch run")

def viper():
    candies = candy()
    print(f'\033[93m{candies[0]}\033[00m')
    print(f'\033[93m{candies[1]}\033[00m')
    print(f'\033[93m{"                 Welcome to Viper CLI. Lets build a project."}\033[00m')
    print()

    project_name = input(f'\033[92m{"Enter project name: "}\033[00m')
    MySql_Database = input(f'\033[92m{"Which MySql Database are you using? "}\033[00m')
    MySql_Username = input(f'\033[92m{"Enter your MySql username: "}\033[00m')
    MySql_Password = input(f'\033[92m{"Enter your MySql password: "}\033[00m')

    global_json() # Create global.json file to specifiy using sdk 2.2.107
    os.system(f"dotnet new mvc --no-https -o {project_name}")
    os.system(f"dotnet add ./{project_name} package Pomelo.EntityFrameworkCore.MySql -v 2.2.0")

    models = []
    print()
    context = input(f'\033[92m{"Enter name of context: "}\033[00m')
    output = build_models(project_name, context)
    models += output[0]

    use_login_and_registration = input(f'\033[92m{"Y/n - Would you like to add Login and Registration? "}\033[00m')

    controller_lines = output[1]
    layout_lines = output[2]

    if use_login_and_registration in ["Y","y","YES","Yes","yes"]:
        use_login_and_registration = True
    else:
        use_login_and_registration = False
    if use_login_and_registration:
        models.append( ("User", "Users") )
        # run login_and_reg codes
        add_login_and_registration(project_name, context, controller_lines)

    # Database relationships
    if len(models) > 1:
        map_database_relationships(project_name, models)

    build_context_file(project_name, context, models)
    build_startup_file(project_name, context)
    if not use_login_and_registration:
        build_controller(project_name, context, controller_lines)
    if use_login_and_registration:
        build_layout(project_name, layout_lines, session=True)
    else:
        build_layout(project_name, layout_lines)
    if not use_login_and_registration:
        build_index(project_name)

    os.system(f"git -C {project_name} init")
    appsettings_json(project_name, MySql_Database, MySql_Username, MySql_Password)
    gitignore(project_name)
    customize_css(project_name)

    # migrations
    wants_to_make_migrations = input(f'\033[92m{"Y/n - Would you like to make migrations? (Not recommended if you want to customize your models further. "}\033[00m')
    if wants_to_make_migrations in ["y","Y","yes","YES","Yes"]:
        make_migrations(project_name, candies[2])
    else:
        print()
        print(f'\033[93m{candies[2]}\033[00m')
        path = f"{pathlib.Path(__file__).parent.absolute()}/{project_name}"
        print(f'\033[93m{"                Thanks for using Viper CLI."}\033[00m')
        print(f'\033[93m{"                  Launching your project..."}\033[00m')
        os.system(f"dotnet watch -p {path} run")

    return True

if __name__ == "__main__":
    viper()

