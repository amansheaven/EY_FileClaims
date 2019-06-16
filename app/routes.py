# from app import app
#from flask import render_template,Flask
import os
#import magic
import urllib.request
from app import app
from flask import Flask, flash, request, redirect, render_template, session
from werkzeug.utils import secure_filename
from app import dep_complete as plate_detect
from app.static.models.pan_detector import detect_card as pan_detect
from app.static.ocr import ocr_textout as ocr
from app.static.ocr import parser as parser
from app.static.ocr import ocr_no_roi as ocr_n

from flask_cachebuster import CacheBuster
from fuzzywuzzy import fuzz, process
import json
import regex

from collections import OrderedDict

config = { 'extensions': ['.jpg', '.png', '.tiff', '.jpeg'], 'hash_size': 4 }

cache_buster = CacheBuster(config=config)

cache_buster.init_app(app)

session_name = 'main'

save_path = 'app/static/'

# class FooStore(object):

#     case = {}
#     @classmethod
#     def get(int):
#         return case

#     @classmethod
#     def set(dict_t):
#         case.update(dict_t)
#         return True
#     @classmethod
#     def prin(int):
#         print(case)
#         return True

# case = FooStore()
case = {}



UPLOAD_FOLDER = 'app/static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


def upload_files(tag, name):
    if request.method == 'POST':
        f = request.files[tag]
        os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'],'unprocessed'), exist_ok=True)
        ext = f.filename.split('.')[1]
        f.save(os.path.join(app.config['UPLOAD_FOLDER'],'unprocessed', secure_filename(name+'.'+ext)))
        print('{} IMAGE UPLOADED'.format(tag))
        # return True

def processor(fun, argg):
    temp = fun.initiate(str(argg))
    return temp


def parse(query,corp,mode):
    return parser.initiate(query,corp,mode)

def dict_pro(corp):
    global case
    case.update({"Claim Number" : parse('claim number',corp,0),
                "Policy Number" : parse('policy/cover note',corp,0),
                "Period of Insurance" : parse ('period of insurance',corp,0),
                "Insured" : parse('insured',corp,0),
                "Registration Number" : parse('registration number',corp,0),
                "Chassis Number" : parse('chassis number',corp,0),
                "Engine Number" : parse('engine number',corp,0),
                "Make" : parse('make',corp,0),
                "Type of Body" : parse('type of body',corp,0),
                "Name of driver" : parse('name of driver',corp,0),
                "Driving Lisence Number" : parse('driving lisence number',corp,0),
                "Date of Issued" : parse('date of issued',corp,0),
                "Valid up to" : parse('valid up to',corp,0),
                "Lisenceing Authority" : parse('lisenceing authority',corp,0),
        })
    return True

def dict_update(dict_to):
    global case
    case = dict_to.copy()
    print(case)


@app.route('/')
def upload_form():
    return render_template('upload.html')

@app.route('/report_detect', methods=['POST'])
def report_ocr():
    if request.method == 'POST':
        upload_files('car-file','car') #2
        upload_files('dl-file','dl') #5
        upload_files('report-file','report') #1
        upload_files('rc-file','rc') #4
        upload_files('pan-file','pan') #3
        upload_files('patch-file','patch') #3


        corp = processor(ocr_n,'report')
        # print('\n\n\n'+corp+'\n\n\n')
        temp_case = {
                "Claim Number" : parse('claim number',corp,0),
                "Policy Number" : parse('policy/cover note',corp,0),
                "Period of Insurance" : parse ('period of insurance',corp,0),
                "Insured" : parse('insured',corp,0),
                "Registration Number" : parse('registration number',corp,0),
                "Chassis Number" : parse('chassis number',corp,0),
                "Engine Number" : parse('engine number',corp,0),
                "Make" : parse('make',corp,0),
                "Type of Body" : parse('type of body',corp,0),
                "Name of driver" : parse('name of driver',corp,0),
                "Driving Lisence Number" : parse('driving lisence number',corp,0),
                "Date of Issued" : parse('date of issued',corp,0),
                "Valid up to" : parse('valid up to',corp,0),
                "Lisenceing Authority" : parse('lisenceing authority',corp,0),
                "Date" : parse('date',corp,0),
        }

        # print("fullfilled :: ",json)
        # print('update ::'+dict_update(temp_case))
        return render_template('template_process.html',im_path = '/static/uploads/unprocessed/report.jpg', outlink = "/car_detect",text = corp, dicti = case, title = 'Report Predictions', dic = temp_case)



@app.route('/car_detect', methods=['POST'])
def upload_file():
    if request.method == 'POST':

        temp_case = {
                "Claim Number" : request.form['Claim Number'],
                "Policy Number" : request.form["Policy Number"],
                "Period of Insurance" : request.form["Period of Insurance"],
                "Insured" : request.form['Insured'],
                "Registration Number" : request.form["Registration Number"],
                "Chassis Number" : request.form["Chassis Number"],
                "Engine Number" : request.form["Engine Number"],
                "Make" : request.form["Make"],
                "Type of Body" : request.form["Type of Body"],
                "Name of driver" : request.form["Name of driver"],
                "Driving Lisence Number" : request.form["Driving Lisence Number"],
                "Date of Issued" : request.form["Date of Issued"],
                "Valid up to" : request.form["Valid up to"],
                "Lisenceing Authority" : request.form["Lisenceing Authority"],
                "Date" : request.form["Date"],
        }
        completeName = os.path.join(save_path, "auth_data.json")
        dat_json = json.dumps(temp_case)
        f = open(completeName,'w+')
        f.write(dat_json)
        f.close()
        with app.open_resource('static/auth_data.json') as f:
            data = json.load(f)
        print(data)
        # data = json.loads(f.read())
        print('EXECUTING')
        update = {}
        for k in list(data.keys()):
            print('CHECK HERE :: '+request.form[k])
            print()
            update.update({
                k:request.form[k]
            })
        completeName = os.path.join(save_path, "auth_data.json")
        dat_json = json.dumps(update)
        f = open(completeName,'w+')
        f.write(dat_json)
        f.close()

        #number = plate_detect.initiate(ext)
        number = "CANNOT DETECT PLATE"
        number = processor(plate_detect, 'jpg')
        file_abs = app.config['UPLOAD_FOLDER']
        file_abs = file_abs.strip('app/')
        proc = os.path.join(file_abs,secure_filename('output_car.jpg'))
        return render_template('car_process.html', im_path = proc, num = number)



@app.route('/pan_detect', methods=['POST'])
def pan_ocr():
    if request.method == 'POST':
        car_info = {
            'Car Verfication Output' : request.form['lis_no']
        }
        print(car_info)
        completeName = os.path.join(save_path, "verify_data.json")
        dat_json = json.dumps(car_info)
        f = open(completeName,'w+')
        f.write(dat_json)
        f.close()
        with app.open_resource('static/auth_data.json') as f:
            data = json.load(f)
            name = data['Name of driver']

        out = processor(pan_detect,'pan')
        corp = processor(ocr,'pan')
        #extract likely feild from authoritative data
        data_dic = {
            'Driver Name' : parse(name.lower(), corp,1)
        }
        #     print('corpu'+corp)
        return render_template('template_process.html',im_path = '/static/uploads/contoured_pan.jpg', text = corp, outlink = "/rc_detect", title = 'PAN Card Predictions', dic = data_dic)
        # return render_template('template_process.html',im_path = '/static/uploads/unprocessed/report.jpg', ,text = corp, dicti = case, title = 'Report Predictions', dic = temp_case)


@app.route('/rc_detect', methods=['POST'])
def rc_ocr():
    if request.method == 'POST':
        pan_info = {
            'PAN Card Name': request.form['Driver Name']
        }
        # print(car_info)
        completeName = os.path.join(save_path, "verify_data.json")
        dat_json = json.dumps(pan_info)
        f = open(completeName,'a')
        f.write("\n"+dat_json)
        f.close()
                
        out = processor(pan_detect,'rc')
        corp = processor(ocr,'rc')
        corp = "\n"+ processor(ocr_n,'rc')
        # reg_no = parse('regn. no', corp,0),
        # print(corp)
        # reg_2nd = parse('registration no.',corp,0)
        # with app.open_resource('static/auth_data.json') as f:
        #     data = json.load(f)
        #     driver_name = data['Registration Number']
        # fin_out = reg_no
        # print(fin_out)
        temp_case = {
            "Registration Number" : parse('regn. no', corp,0),
            "Chassis Number" : parse('ch. no',corp,0),
            "Engine Number" : parse('e no',corp,0),
            "Name" : parse('name',corp,0),
        }
        return render_template('template_process.html',im_path = '/static/uploads/contoured_rc.jpg', text = corp, outlink = "/dl_detect", title = 'RC Card Predictions', dic = temp_case)

@app.route('/dl_detect', methods=['POST'])
def dl_ocr():
    if request.method == 'POST':
        rc_info = {
            "RC Registration Number" : request.form['Registration Number'],
            "RC Chassis Number" :request.form['Chassis Number'],
            "RC Engine Number" : request.form['Engine Number'],
            "RC Name" : request.form['Name'],
        }
        completeName = os.path.join(save_path, "verify_data.json")
        dat_json = json.dumps(rc_info)
        f = open(completeName,'a')
        f.write("\n"+dat_json)
        f.close()

        out = processor(pan_detect,'dl')
        corp = processor(ocr,'dl')
        corp = "\n"+ processor(ocr_n,'dl')

        temp_case = {
            "DL No" : parse('DL No.', corp,0),
            "Date of Issue" : parse('doi', corp, 0),
            "Valid Till" : parse('valid till',corp,0),
            "Name" : parse('name',corp,0),
        }
        return render_template('template_process.html',im_path = '/static/uploads/contoured_dl.jpg', text = corp, outlink = "/patch_detect", title = 'DL Card Predictions', dic = temp_case)



@app.route('/patch_detect', methods=['POST'])
def patch_ocr():
    if request.method == 'POST':
        rc_info = {
            "DL Registration Number" : request.form['DL No'],
            "DL Date of Issue" :request.form['Date of Issue'],
            "DL Valid Till" : request.form['Valid Till'],
            "Dl Name" : request.form['Name'],
        }
        completeName = os.path.join(save_path, "verify_data.json")
        dat_json = json.dumps(rc_info)
        f = open(completeName,'a')
        f.write("\n"+dat_json)
        f.close()

        out = processor(pan_detect,'patch')
        corp = processor(ocr,'patch')
        corp = "\n"+ processor(ocr_n,'patch')

        temp_case = {
            "Chasis Number" : parse('vin',corp,0),
        }
        return render_template('template_process.html',im_path = '/static/uploads/contoured_patch.jpg', text = corp, outlink = "/result", title = 'Car Patch Predictions', dic = temp_case)

        # return render_template('template_process.html',im_path = '/static/uploads/contoured_dl.jpg', text = corp, outlink = "/dl_detect", title = 'DL Card Predictions', dic = temp_case)


@app.route('/result', methods=['POST'])
def result():
    if request.method == 'POST':
        patch_info = {
            "Patch Chasis Number" : request.form['Chasis Number'],
        }
        completeName = os.path.join(save_path, "verify_data.json")
        dat_json = json.dumps(patch_info)
        f = open(completeName,'a')
        f.write("\n"+dat_json)
        f.close()

        with app.open_resource('static/verify_data.json',mode = 'r') as f:
            verify_data = f.read()
            verify_data = verify_data.split('\n')
            verify_data = list(OrderedDict.fromkeys(verify_data))
            print(verify_data)

        
        with app.open_resource('static/auth_data.json',mode = 'r') as f:
            auth_data = json.load(f)
            print(auth_data)

        completeName = os.path.join(save_path, "verify_data.json")
        f = open(completeName,'w').close()

        completeName = os.path.join(save_path, "auth_data.json")
        f = open(completeName,'w').close()
        print('removed jsons')
        #         upload_files('car-file','car') #2
        # upload_files('dl-file','dl') #5
        # upload_files('report-file','report') #1
        # upload_files('rc-file','rc') #4
        # upload_files('pan-file','pan') #3
        # upload_files('patch-file','patch') #3

        list_i=['Car Image', 'PAN Card', 'RC Card', 'DL Card', 'Patch']

        return render_template('result.html', title = 'Result Page', auth_data = auth_data, v_data = verify_data,list_i = list_i,auth_var ="Authoritative Report Data")
        