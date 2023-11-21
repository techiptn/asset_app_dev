from flask import Flask, render_template, redirect, url_for, send_file
from flask_bootstrap import Bootstrap
from form import AssetForm, EditForm
from csvcontrol import *
import pandas as pd
pd.set_option('display.precision', 2)
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWligakeiKKiekSihBXox7C0sKR6b'
Bootstrap(app)

assetdata = 'data/test.csv'
userdata = 'data/userinfo.csv'

@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=["GET", "POST"])
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
            return redirect(url_for('showlist'))
        return redirect(url_for('userid_error'))
    return render_template('add.html', form=form)


@app.route('/error')
def userid_error():
    return render_template('error.html')


@app.route('/edit/<int:code>', methods=["GET", "POST"])
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
            valuedict['AcquisitionValue(CAD)'] = form.a_value.data
            valuedict['Tax'] = form.a_tax.data
            valuedict['Com1'] = form.com1.data
            valuedict['Com2'] = form.com2.data
            valuedict['Status'] = form.status.data
            data_edit(userdata)
            data_update(assetdata, valuedict)
            indextrim(assetdata)
            return redirect(url_for('showlist'))
        return redirect(url_for('userid_error'))
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
    form.a_value.default = values2[8]
    form.a_tax.default = values2[9]
    form.com1.default = values2[13]
    form.com2.default = values2[14]
    form.status.default = int(values2[15])
    form.process()
    return render_template('edit.html', form=form)


@app.route('/table')
def pdtable():
    df = pd.read_csv(assetdata, index_col=0)
    return render_template('pdtable.html', tables=[df.to_html(classes='mystyle')], titles=df.columns.values)


@app.route('/assets')
def showlist():
    with open(assetdata, newline='') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template(
        'assets.html', col=list_of_rows[0], assets=list_of_rows[1::], n = 0
        )


@app.route('/download')
def downloadFile():
    #For windows you need to use drive name [ex: F:/Example.pdf]
    rename = 'IT_asset_'+datetime.datetime.now().strftime("%Y-%m-%d")+'.csv'
    path = assetdata
    return send_file(path, as_attachment=True, attachment_filename = rename)


if __name__ == '__main__':
    app.run(debug=True)
