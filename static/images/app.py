
# A very simple Flask Hello World app for you to get started with...

from flask import Flask
from flask import url_for,request,render_template,redirect,session,jsonify,flash
#from db import dbconnect
from functools import wraps
#from database_interaction import login_authentication
#from database_interaction import registration_authentication
#from database_interaction import upload_new_product,insert_register_user
import database_interaction
from database_interaction import InsertPartner
#from mail import Email_verification
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'mysite/static/images/lights/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}



app = Flask(__name__)

app.secret_key="abcdffgdefgac"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
'''
@app.route('/')
def hello_world():
    return 'Hello from Flask!'
'''
'''********************************Admin Part***********************************************'''
def alogin_required(f):
    @wraps(f)
    def wrap(*args ,**kwargs):
        if 'admin_vishal_gupta_lighthub.com_with_other_3' in session:
            return f(*args ,**kwargs)
        else:
            flash('Please Logged In Yourself')
            return redirect(url_for('adminlogin'))
    return wrap

def already_login(f):
    @wraps(f)
    def wrap(*args ,**kwargs):
        if 'admin_vishal_gupta_lighthub.com_with_other_3' in session:
            flash('You are already loggedin')
            return redirect(url_for('adminhome'))
        else:
            return redirect(url_for('adminlogin'))
    return wrap

@app.route('/logout')
@alogin_required
def logout():
    session.clear()
    flash('You Have successfully LoggedOut')
    return redirect(url_for('adminlogin'))

@app.route('/',methods=['GET','POST'])
def adminlogin():
    if request.method == 'POST':
        username =request.form['username']
        password = request.form['password']

        if username == "lighthub.com" and password == 'light':
            session['admin_vishal_gupta_lighthub.com_with_other_3']=True
            session['adminusername'] = username
            flash('You Have successfully Logged In')
            return redirect(url_for('adminhome'))
        else:
            return render_template('admin/adminlogin.html',elem='WP')
    else:
        return render_template('admin/adminlogin.html')


@app.route('/adminhome',methods=['GET','POST'])
@alogin_required
def adminhome():
    return render_template('admin/adminhome.html')


@app.route('/InsertNewProduct',methods=['GET','POST'])
@alogin_required
def InsertNewProduct():
    return render_template('admin/InsertNewProduct.html')

@app.route('/UpdateProductDetails',methods=['GET','POST'])
@alogin_required
def UpdateProductDetails():
    return render_template('admin/UpdateproductDetails.html')

@app.route('/RemoveProduct',methods=['GET','POST'])
@alogin_required
def RemoveProduct():
    return render_template('admin/RemoveProduct.html')

def encryption(val):
    val=val.lower()
    val=val.strip()
    nval=''

    for i in val:
        if i!= " ":
            nval=nval+str(ord(i))
    return nval

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        ProductImage= request.files['file']
        ProductImage1=request.files['file1']
        ProductName=request.form['ProductName'].lower()
        ProductId=encryption(ProductName)
        #print(ProductId)
        ProductType=request.form['ProductType']
        ProductType1=request.form['ProductType1']
        ProductSpecification=request.form['ProductSpecification']
        ProductPrice=request.form['ProductPrice']
        ProductWarranty=request.form['ProductWarranty']
        ProductBrand=request.form['ProductBrand']

        filename = secure_filename(ProductImage.filename)
        filename1 = secure_filename(ProductImage1.filename)
        ProductImageAddress="static/images/lights/"+filename;
        ProductImageAddress1="static/images/lights/"+filename1
        response=database_interaction.upload_new_product(ProductId,ProductName,ProductType,ProductWarranty,ProductSpecification,ProductPrice,ProductImageAddress,ProductImageAddress1,ProductType1,ProductBrand)
        if response == 'success':
            ProductImage.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            ProductImage1.save(os.path.join(app.config['UPLOAD_FOLDER'], filename1))
            flash('Product Sucessfully Added')
            return redirect(url_for('InsertNewProduct'))
        else:
            flash('Product Already Present!')
            return redirect(url_for('InsertNewProduct'))

    else:
        flash('Product Already Present!')
        return render_template('admin/adminhome.html')


@app.route('/admin/AddPartner',methods=['GET','POST'])
@alogin_required
def AddPartner():
    return render_template('admin/AddPartner.html')

@app.route('/admin/AddPartnerProcess',methods=['GET','POST'])
def AddPartnerProcess():
    if request.method == 'POST':
        EnterpriseName=request.form['EnterpriseName']
        OwnerName=request.form['OwnerName'].lower()
        Contact1=request.form['Contact1'].lower()
        Contact2=request.form['Contact2'].lower()
        Contact3=request.form['Contact3'].lower()
        Address=request.form['Address'].lower()
        # for optinal mobile Number
        if len(Contact2) == 0:
            Contact2='-'
        result=InsertPartner(EnterpriseName,OwnerName,Contact1,Contact2,Contact3,Address)
        if result=='success':
            flash('Partner Added Successfully')
            return redirect(url_for('AddPartner'))
            #return render_template('Admin/AddPartner.html',elem='added')
        else:
            return redirect(url_for('exception'))

    else:
        return redirect(url_for('AddPartner'))






@app.route('/admin/PartnerManagement',methods=['GET','POST'])
@alogin_required
def PartnerManagement():
    return render_template('admin/PartnerManagement.html')


@app.route('/update_detail_page_transfer',methods=['GET','POST'])
@alogin_required
def update_detail_page_transfer():
    if request.method == 'POST':
        hiddenpid=request.form['pid']
        print("hello_world")
        return redirect(url_for('updetails',pid=hiddenpid))

@app.route('/updetails/<pid>/')
@alogin_required
def updetails(pid):
    return render_template('admin/updetails.html',pid=pid)
'''***********************************EXCEPTIONS******************************************'''
@app.route('/exception',methods=['GET','POST'])
def exception():
    return render_template('exception.html')



'''*************************************DB CONNECTIVITY ADMIN PART******************************************'''
@app.route('/get_Details_of_Partners',methods=['GET','POST'])
def get_Details_of_Partners():
    if request.method == 'POST':
        partner_list=[]
        PartnerDetails=database_interaction.LoadPartners()
        for partner in PartnerDetails:
            partner_list.append({"EnterpriseId":partner[0],"EnterpriseName":partner[1],"OwnerName":partner[2],"Contact1":partner[3],"Contact2":partner[4],"Contact3":partner[5],"Address":partner[6]})

        dic={"Info":partner_list}
        return jsonify(dic)

@app.route('/get_Details_of_Individual_Partners',methods=['GET','POST'])
def get_Details_of_Individual_Partners():
    if request.method == 'POST':
        postData = request.form['pid']
        #print("sdjbkjdk",postData)
        #print(type(postData))
        partner=database_interaction.LoadIndividualPartners(postData)
        partner={"EnterpriseId":partner[0],"EnterpriseName":partner[1],"OwnerName":partner[2],"Contact1":partner[3],"Contact2":partner[4],"Contact3":partner[5],"Address":partner[6]}

        dic={"Info":partner}
        return jsonify(dic)

@app.route('/remove_partner',methods=['GET','POST'])
def remove_partner():
    if request.method == 'POST':
        postData = request.form['pid']
        partner=database_interaction.RemovePartner(postData)
        if partner == '1':
            flash('Partner Successfully Removed.')
            return redirect(url_for('PartnerManagement'))
        else:
            return redirect(url_for('exception'))


@app.route('/get_LoadProduct',methods=['GET','POST'])
def get_LoadProduct():
    if request.method == 'POST':
        postdata = request.form['option']
        postdata1=request.form['option1']
        #print(postdata)
        product_list1=[]
        products=database_interaction.LoadProduct(postdata,postdata1)
        #print(products)
        for product in products:
            product_list1.append({'id':product[0],'ProductId':product[1],'ProductName':product[2],
                'ProductType':product[3],'ProductWarranty':product[4],
                'ProductSpecification':product[5],
                'ProductPrise':product[6],'ProductImageAddress':product[7],
                'ProductImageAddress1':product[8],'ProductType1':product[9],
                'ProductBrand':product[10],'addeddate':product[11]})
    dic={"Info":product_list1}
    return jsonify(dic)

@app.route('/remove_product',methods=['GET','POST'])
def remove_product():
    if request.method == 'POST':

        postData = request.form['pid']
        #print("sdjbkjdk",postData)
        partner=database_interaction.RemoveProduct(postData)
        if partner == '1':
            flash('Product Successfully Removed.')
            return redirect(url_for('RemoveProduct'))
        else:
            return redirect(url_for('exception'))


@app.route('/get_details_of_product',methods=['GET','POST'])
def get_Details_of_Product():
    if request.method == 'POST':

        postData = request.form['pid']
        #print("sdjbkjdk111111111111",postData)
        product=database_interaction.ProductDetails(postData)
        print(product)
        product={'ProductId':product[1],'ProductName':product[2],
                'ProductType':product[3],'ProductWarranty':product[4],
                'ProductSpecification':product[5],
                'ProductPrise':product[6],'ProductImageAddress':product[7],
                'ProductImageAddress1':product[8],'ProductType1':product[9],
                'ProductBrand':product[10],'addeddate':product[11]}
        dic={"Info":product}
        return jsonify(dic)

@app.route('/update_price',methods=['GET','POST'])
def update_price():
    if request.method == 'POST':
        hiddenpid=request.form['pid']
        ud=request.form['updateddetails']
        result=database_interaction.update_product_price(hiddenpid,ud)
        if result == 'success':
            dic={'Info':"1"}
            return jsonify(dic)

@app.route('/update_name',methods=['GET','POST'])
def update_name():
    if request.method == 'POST':
        hiddenpid=request.form['pid']
        ud=request.form['updateddetails']
        result=database_interaction.update_product_name(hiddenpid,ud)
        if result == 'success':
            dic={'Info':"1"}
            return jsonify(dic)

@app.route('/update_type',methods=['GET','POST'])
def update_type():
    if request.method == 'POST':
        hiddenpid=request.form['pid']
        ud=request.form['updateddetails']
        print(ud)
        result=database_interaction.update_product_type(hiddenpid,ud)
        if result == 'success':
            dic={'Info':"1"}
            return jsonify(dic)


@app.route('/update_type1',methods=['GET','POST'])
def update_type1():
    if request.method == 'POST':
        hiddenpid=request.form['pid']
        ud=request.form['updateddetails']
        result=database_interaction.update_product_type1(hiddenpid,ud)
        if result == 'success':
            dic={'Info':"1"}
            return jsonify(dic)


@app.route('/update_brand',methods=['GET','POST'])
def update_brand():
    if request.method == 'POST':
        hiddenpid=request.form['pid']
        ud=request.form['updateddetails']
        result=database_interaction.update_product_brand(hiddenpid,ud)
        if result == 'success':
            dic={'Info':"1"}
            return jsonify(dic)

@app.route('/update_warranty',methods=['GET','POST'])
def update_warranty():
    if request.method == 'POST':
        hiddenpid=request.form['pid']
        ud=request.form['updateddetails']
        result=database_interaction.update_product_warranty(hiddenpid,ud)
        if result == 'success':
            dic={'Info':"1"}
            return jsonify(dic)

@app.route('/update_description',methods=['GET','POST'])
def update_description():
    if request.method == 'POST':
        hiddenpid=request.form['pid']
        ud=request.form['updateddetails']
        result=database_interaction.update_product_description(hiddenpid,ud)
        if result == 'success':
            dic={'Info':"1"}
            return jsonify(dic)

@app.route('/update_image1',methods=['GET','POST'])
def update_image1():
    if request.method == 'POST':
        if 'file' in request.files and "pid" in request.form:
            hiddenpid=request.form['pid']
            #print(request.form)
            #print(request.files)
            ProductImage=request.files['file']
            filename = secure_filename(ProductImage.filename)
            ProductImageAddress="static/images/lights/"+filename;

            result=database_interaction.update_product_image1(hiddenpid,ProductImageAddress)
            if result == 'success':
                ProductImage.save(os.path.join(app.config['UPLOAD_FOLDER'], filename));
                dic={'Info':"1"}
                return jsonify(dic)

        dic={'Info':"0"}
        return jsonify(dic)

@app.route('/update_image2',methods=['GET','POST'])
def update_image2():
    if request.method == 'POST':
        if 'file1' in request.files and "pid" in request.form:
            hiddenpid=request.form['pid']
            #print(request.form)
            #print(request.files)
            ProductImage=request.files['file1']
            filename = secure_filename(ProductImage.filename)
            ProductImageAddress="static/images/lights/"+filename;

            result=database_interaction.update_product_image2(hiddenpid,ProductImageAddress)
            if result == 'success':
                ProductImage.save(os.path.join(app.config['UPLOAD_FOLDER'], filename));
                dic={'Info':"1"}
                return jsonify(dic)

        dic={'Info':"0"}
        return jsonify(dic)

