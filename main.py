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
        data_fillup(assetdata, userdata)
        data_update(assetdata, valuedict)
        return redirect(url_for('pdtable'))
    return render_template('add.html', form=form)


@app.route('/edit', methods=["GET", "POST"])
def edit_info():
    form = EditForm()
    if form.validate_on_submit():
        with open(assetdata, mode="a") as csv_file:
            csv_file.write(
                f"\n{form.cafe.data},"
                f"{form.location.data},"
                f"{form.open.data},"
                f"{form.close.data},"
                f"{form.coffee_rating.data},"
                f"{form.wifi_rating.data},"
                f"{form.power_rating.data}"
                )
        return redirect(url_for('pdtable'))
    return render_template('edit.html', form=form)


@app.route('/table')
def pdtable():
    df = pd.read_csv(assetdata)
    return render_template('pdtable.html', tables=[df.to_html(classes='mystyle')], titles=df.columns.values)



@app.route('/assets')
def showlist():
    with open(assetdata, newline='') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template(
        'assets.html', col=list_of_rows[0], assets=list_of_rows[1::]
        )

@app.route('/download')
def downloadFile():
    #For windows you need to use drive name [ex: F:/Example.pdf]
    rename = 'IT_asset_'+datetime.datetime.now().strftime("%Y-%m-%d")+'.csv'
    path = assetdata
    return send_file(path, as_attachment=True, attachment_filename = rename)


if __name__ == '__main__':
    app.run(debug=True)
