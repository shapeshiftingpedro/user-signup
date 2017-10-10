from flask import Flask, request, redirect, render_template
import cgi
import jinja2

app = Flask(__name__)

app.config["DEBUG"] = True


@app.route("/signin", methods=["POST"])
def new_sign_in():
    new_user = request.form["new-user"]

    e_mail_addr = request.form["mail-me"]

    new_pass = request.form["secret"]

    new_pass_confirm = request.form["code"]
    #easter eggs are fun, aren't they?

    #wall-of-checks
    is_error = False
    user_error = ""
    user_error_char = ""
    user_error_space = ""
    pass_error_space = ""
    pass_error = ""
    pass_error_char = ""
    conf_error = ""
    e_error_space = ""
    e_error = ""

    if (not new_user) or (new_user.strip() == ""):
        user_error = "Please specify the username you wish to have."
        is_error = True
        

    if not len(new_user) >= 3 and len(new_user) <= 20:
        user_error_char = "Please choose a Username between 3 and 20 characters long."
        is_error = True

    if " " in new_user:
        user_error_space = "Please do not include any spaces in your username."
        is_error = True

    if " " in new_pass:
        pass_error_space = "Please do not include any spaces in your password."
        is_error = True

    if (not new_pass) or (new_pass.strip() == ""):
        pass_error = "Please specify your password."
        is_error = True 

    if not len(new_pass) >= 3 and len(new_pass) <= 20:
        pass_error_char = "Please choose a Password between 3 and 20 characters long."
        is_error = True

    if (not new_pass_confirm) or (new_pass_confirm.strip() == "") or (new_pass != new_pass_confirm):
        conf_error = "Please confirm your password."
        is_error = True

    if (not e_mail_addr.strip() == ""):
        #run email verifs
        if " " in e_mail_addr:
            e_error_space = "Please do not include spaces in the E-mail Address."
            is_error = True

        if not ("@" in e_mail_addr and "." in e_mail_addr and len(e_mail_addr) >= 3 and len(e_mail_addr) <= 20):
            e_error = "Please use a valid E-mail Address."
            is_error = True

    new_user_esc = cgi.escape(new_user, quote=True)

    e_mail_addr_esc = cgi.escape(e_mail_addr, quote=True)

    new_pass_esc = cgi.escape(new_pass, quote=True)

    new_pass_confirm_esc = cgi.escape(new_pass_confirm, quote=True)

    if is_error:
        return render_template("signin.html", user_error=user_error, user_error_char=user_error_char, user_error_space=user_error_space, pass_error_space=pass_error_space, pass_error=pass_error, pass_error_char=pass_error_char, conf_error=conf_error, e_error_space=e_error_space, e_error=e_error)
    else:
        return render_template("signin-confirmed.html", new_user=new_user_esc)


@app.route("/")
def index():
    encoded_error = request.args.get("error")
    return render_template("signin.html", error = encoded_error and cgi.escape(encoded_error, quote=True))


app.run()