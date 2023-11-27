from flask import Flask, render_template, redirect, url_for, send_file, request
from flask_bootstrap import Bootstrap
from form import AssetForm, EditForm
from csvcontrol import *
from module import *
import pandas as pd
# pd.set_option('display.precision', 2)

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWligakeiKKiekSihBXox7C0sKR6b'
Bootstrap(app)

assetdata = 'data/test.csv'
userdata = 'data/userinfo2.csv'
validdata = 'data/valid_only.csv'
bkpath = 'data/bk'
labelpath = 'data/label'

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
            indextrim(assetdata)
            return redirect(url_for('showlist'))
        return redirect(url_for('userid_error'))
    return render_template('add.html', form=form)


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
        return redirect(url_for('userid_error', userinfo = form.user.data))
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
def pdtable():
    df = pd.read_csv(assetdata, index_col=0)
    return render_template('pdtable.html', tables=[df.to_html(classes='mystyle')], titles=df.columns.values)


@app.route('/delete/<int:code>', methods=["GET", "POST"])
def delete_item(code):
    data_delete(code, assetdata)
    return redirect(url_for('raw_edit'))
    

@app.route('/assets')
def showlist():
    list_1 = filter_list(assetdata)
    list_v = dp_convert(list_1)
    return render_template(
        'assets.html', col=list_v[0], assets=list_v[1], n = 0)


@app.route('/raw_edit')
def raw_edit():
    df = pd.read_csv(assetdata, index_col=0)
    list_v = dp_convert(df)
    return render_template(
        'rawedit.html', col=list_v[0], assets=list_v[1], n = 0)


@app.route('/checkbox', methods=["GET", "POST"])
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


@app.route('/error/<userinfo>')
def userid_error(userinfo):
    return render_template('error.html', userinfo = userinfo)


@app.route('/download')
def downloadFile():
    #For windows you need to use drive name [ex: F:/Example.pdf]
    rename = 'IT_asset_raw_'+datetime.datetime.now().strftime("%Y-%m-%d")+'.csv'
    path = assetdata
    return send_file(path, as_attachment=True, download_name=rename)


@app.route('/valid_only')
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
