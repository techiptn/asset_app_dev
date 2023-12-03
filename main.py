from flask import Flask, render_template, redirect, url_for, send_file, request,flash
from flask_bootstrap import Bootstrap
from flask_login import login_user, UserMixin, LoginManager, login_required, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from form import AssetForm, EditForm, UserForm, LoginForm
from config import users_db
from csvcontrol import *
from module import *
import pandas as pd
# pd.set_option('display.precision', 2)

app = Flask(__name__)
app.config.from_object('config.Config')
# app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWligakeiKKiekSihBXox7C0sKR6b'
Bootstrap(app)
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(userid):
    return User(userid)

class User(UserMixin):
    def __init__(self, username):
        self.id = username
        self.password = users_db[username]
        
    def __repr__(self):
        return "%s/%s" % ( self.id, self.password)
    
    def is_active(self):
        return True


assetdata = 'data/test.csv'
userdata = 'data/userinfo2.csv'
validdata = 'data/valid_only.csv'
labelpath = 'data/label'


@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # ID doesn't exist
        if not form.ID.data in [x for x in users_db.keys()]:
            flash("ID does not exist, please try again.")
            return redirect(url_for('login'))
        user = User(form.ID.data)
        password = form.password.data
        # Password incorrect
        if not check_password_hash(user.password, password):
            flash("Password incorrect, please try again.")
            return redirect(url_for('login'))
        else:
            login_user(user)
            return redirect(url_for('home'))
    return render_template("login.html", form=form, logged_in=current_user.is_authenticated)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home', logged_in=current_user.is_authenticated))

@app.route("/")
def home():
    return render_template("index.html", logged_in=current_user.is_authenticated)


@app.route('/add', methods=["GET", "POST"])
@login_required
def add_info():
    form = AssetForm()
    if form.validate_on_submit():
        if validate_userid(form.user.data, userdata):
            valuedict['Date'] = form.date.data
            valuedict['AcquisitionType'] = form.a_type.data
            valuedict['DeviceType'] = form.d_type.data
            valuedict['AcquisitionLocation'] = form.a_loca.data
            valuedict['Manufacturer'] = form.manufac.data
            valuedict['SN'] = form.sn.data
            valuedict['UserID'] = form.user.data
            valuedict['CurrentLocation'] = form.c_loca.data
            valuedict['AcquisitionValue(CAD)'] = form.a_value.data
            valuedict['Tax'] = form.a_tax.data
            valuedict['Com1'] = form.com1.data
            valuedict['Com2'] = form.com2.data
            valuedict['Status'] = form.status.data
            data_fillup(assetdata, userdata)
            data_update(assetdata, valuedict)
            indextrim(assetdata)
            return redirect(url_for('showlist'))
        flash(f'!? {form.user.data} is not existing in the user list, please check it again')
        return redirect(url_for('userlist'))
        # return redirect(url_for('userid_error', userinfo = form.user.data))
    form.user.default = 'IT'
    form.process()
    return render_template('add.html', form=form, logged_in=current_user.is_authenticated)


@app.route('/edit/<int:code>', methods=["GET", "POST"])
@login_required
def edit_info(code):
    form = EditForm()
    if form.validate_on_submit():
        if validate_userid(form.user.data, userdata):
            valuedict['AssetCode'] = form.a_code.data
            valuedict['Date'] = form.date.data
            valuedict['AcquisitionType'] = form.a_type.data
            valuedict['DeviceType'] = form.d_type.data
            valuedict['AcquisitionLocation'] = form.a_loca.data
            valuedict['Manufacturer'] = form.manufac.data
            valuedict['SN'] = form.sn.data
            valuedict['UserID'] = form.user.data
            valuedict['CurrentLocation'] = form.c_loca.data
            valuedict['PurchasePrice(+Tx)'] = form.t_value.data
            valuedict['AcquisitionValue(CAD)'] = form.a_value.data
            valuedict['Tax'] = form.a_tax.data
            valuedict['Com1'] = form.com1.data
            valuedict['Com2'] = form.com2.data
            valuedict['Status'] = form.status.data
            data_edit(userdata)
            data_update(assetdata, valuedict)
            indextrim(assetdata)
            return redirect(url_for('showlist'))
        flash(f'!? {form.user.data} is not existing in the user list, please check it again')
        return redirect(url_for('userlist'))
        # return redirect(url_for('userid_error', userinfo = form.user.data))
    values2 = code_data_dic(code, assetdata)
    form.a_code.default = values2[0]
    form.date.default = values2[1]
    form.a_type.default = values2[2]
    form.d_type.default = values2[3]
    form.a_loca.default = values2[4]
    form.manufac.default = values2[5]
    form.sn.default = values2[6]
    form.user.default = values2[10]
    form.c_loca.default = values2[12]
    form.t_value.default = values2[7]
    form.a_value.default = values2[8]
    form.a_tax.default = values2[9]
    form.com1.default = values2[13]
    form.com2.default = values2[14]
    form.status.default = int(values2[15])
    form.process()
    return render_template('edit.html', form=form)

#Just for referance (Panda table veiwing)
@app.route('/table')
@login_required
def pdtable():
    df = pd.read_csv(assetdata, index_col=0)
    return render_template('pdtable.html', tables=[df.to_html(classes='mystyle')], titles=df.columns.values)


@app.route('/delete/<int:code>', methods=["GET", "POST"])
@login_required
def delete_item(code):
    data_delete(code, assetdata, 'asset')
    return redirect(url_for('raw_edit'))


@app.route('/deleteuser/<int:code>', methods=["GET", "POST"])
@login_required
def delete_user(code):
    data_delete(code, userdata, 'user')
    return redirect(url_for('userlist'))


@app.route('/assets')
@login_required
def showlist():
    list_1 = filter_list(assetdata)
    list_v = dp_convert(list_1)
    return render_template(
        'assets.html', col=list_v[0], assets=list_v[1], n = 0)


@app.route('/raw_edit')
@login_required
def raw_edit():
    df = pd.read_csv(assetdata, index_col=0)
    list_v = dp_convert(df)
    return render_template(
        'rawedit.html', col=list_v[0], assets=list_v[1], n = 0)

#Create Label
@app.route('/checkbox', methods=["GET", "POST"])
@login_required
def checkbox():
    if request.method == 'POST' and len(request.form.getlist('selected')) > 0:
        cleanupfolder(labelpath)
        qlist = request.form.getlist('selected')
        qr_img_dict = qr_sv_img(assetdata, qlist)
        for i in qr_img_dict.keys():
            qr_img_dict[i].save(f'{labelpath}/{i}.png')
        stream = zipfiles(labelpath)
        return send_file(stream, as_attachment=True, 
                            download_name='labels.zip'
                        )
    list_1 = filter_list(assetdata)
    list_v = dp_convert(list_1)
    return render_template(
        'checkbox.html', col=list_v[0], assets=list_v[1], n = 0)

#User info management
@app.route('/user')
@login_required
def userlist():
    list_1 = pd.read_csv(userdata, index_col=0)
    list_v = dp_convert(list_1)
    return render_template(
        'userlist.html', col=list_v[0], assets=list_v[1], n = 0)


@app.route('/user_add', methods=["GET", "POST"])
@login_required
def add_user():
    form = UserForm()
    if form.validate_on_submit():
        id = form.userid.data
        name = form.username.data
        adduser(id, name, userdata)
        return redirect(url_for('userlist'))
    return render_template('adduser.html', form=form)


@app.route('/useredit/<int:code>', methods=["GET", "POST"])
@login_required
def useredit_info(code):
    form = UserForm()
    if form.validate_on_submit():
        id = form.userid.data
        name = form.username.data
        data_delete(code, userdata, 'user')
        adduser(id, name, userdata)
        return redirect(url_for('userlist'))
    values2 = code_user(code, userdata)
    form.userid.default = values2[0]
    form.username.default = values2[1]
    form.process()
    return render_template('edit.html', form=form)

'''
@app.route('/error/<userinfo>')
def userid_error(userinfo):
    return render_template('error.html', userinfo = userinfo)
'''

@app.route('/download')
@login_required
def downloadFile():
    #For windows you need to use drive name [ex: F:/Example.pdf]
    rename = 'IT_asset_raw_'+datetime.datetime.now().strftime("%Y-%m-%d")+'.csv'
    path = assetdata
    return send_file(path, as_attachment=True, download_name=rename)


@app.route('/valid_only')
@login_required
def valid_only():
    #For windows you need to use drive name [ex: F:/Example.pdf]
    rename = 'IT_asset_valid_only'+datetime.datetime.now().strftime("%Y-%m-%d")+'.csv'
    datapd = filter_list(assetdata)
    datapd2 = datapd.loc[:, ~datapd.columns.str.contains('^Unnamed')]
    datapd2.to_csv(validdata)
    path = validdata
    return send_file(path, as_attachment=True, download_name= rename)


if __name__ == '__main__':
    app.run(debug=True)
