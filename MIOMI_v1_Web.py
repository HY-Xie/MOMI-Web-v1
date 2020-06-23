from flask import Flask, render_template, redirect, url_for, request, session
import config
from models import Employee, Customer, Glass, Eyedrop, Nursing, Washing, Consumption, EmployeeLog
from exts import db 
import datetime

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)

def writeEmployeeLog(employeeId, operation, content):
    employee = Employee.query.filter(Employee.id == employeeId).first()
    employeeName = employee.name
    log = EmployeeLog(employeeId=employeeId, time=datetime.datetime.now(), employeeName=employeeName, operation=operation, content=content)
    db.session.add(log)
    db.session.commit()


@app.route('/')
def index():
    if 'employee_id' in session:
        return render_template('index.html')
    else:
        return redirect(url_for('login'))
    


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        cellphone = request.form.get('cellphone')
        password = request.form.get('password')
        employee = Employee.query.filter(Employee.cellphone == cellphone, Employee.password == password).first()

        if employee:    # 登录成功
            if employee.duty == 'dimission':    # 离职无法登录
                return redirect(url_for('login'))
            # 正常登录 - 记录cookie
            session['employee_id'] = employee.id 
            # print("session['employee_id']", session['employee_id'])
            print(session['employee_id'])
            writeEmployeeLog(employee.id, '登录', 'None')
            return redirect(url_for('index'))
        else:
            return u'手机号或密码错误'
        
@app.route('/logout/')
def logout():
    # session.pop('employee_id')
    # del session['employee_id']
    writeEmployeeLog(session.get('employee_id'), '注销', 'None')
    session.clear()
    # print('session: ', session.get('employee_id'))
    
    return redirect(url_for('login'))


@app.route('/addcustomer/', methods=['GET', 'POST'])
def addcustomer():
    if session.get('employee_id') is None:
        return redirect(url_for('login'))
    if request.method == 'GET':
        numOfCustomer = len(Customer.query.filter().all())
        return render_template('addcustomer.html')
    else:
        cellphone = request.form.get('cellphone')
        if len(cellphone) != 11:
            return u'错误:需输入11位手机号码'
        name = request.form.get('name')
        wechat = request.form.get('wechat')
        email = request.form.get('email')
        myopia = [request.form.get('left_myopia'), request.form.get('right_myopia')]
        astig = [request.form.get('left_astig'), request.form.get('right_astig')]
        if myopia[0] == '':
            myopia[0] = '0'
        if myopia[1] == '':
            myopia[1] = '0'
        if astig[0] == '':
            astig[0] = '0'
        if astig[1] == '':
            astig[1] = '0'
        score = 0
        purchase = 0
        password = '8888'
        
        hasCustomer = Customer.query.filter(Customer.cellphone == cellphone).first()
        if hasCustomer:
            return u'手机号码已存在'
        else:
            newCustomer = Customer(cellphone = cellphone,
                        name = name,
                        wechat = wechat,
                        email = email,
                        left_myopia = myopia[0],
                        right_myopia = myopia[1],
                        left_astig = astig[0],
                        right_astig = astig[1],
                        score = score,
                        purchase = purchase,
                        password = password )
            db.session.add(newCustomer)
            db.session.commit()
        operation = u'新增会员'
        content = cellphone + ' ' + name
        writeEmployeeLog(session.get('employee_id'), operation, content)
        return redirect(url_for('index'))


@app.route('/glassSKU/', methods=['GET', 'POST'])
def glassSKU():
    if session.get('employee_id') is None:
        return redirect(url_for('login'))
    if request.method == 'GET':
        
        # print(type(glasses))
        # print(glasses)
        glasses = Glass.query.filter().all()
        return render_template('glassSKU.html', glasses = glasses)
    else:
        brand = request.form.get('brandSelect')
        model = request.form.get('glassModel')
        color = request.form.get('glassColor')
        degree = request.form.get('glassDegree')
        amount = request.form.get('glassAmount')
        
        if brand == '' or color == '' or degree == '' or amount == '' or model=='':
            glasses = Glass.query.filter().all()
            return render_template('glassSKU.html', glasses = glasses)
        else:
            if color[-1] == u'色':
                color = color[0:len(color)-1]
        sku = brand + '-' + model + '-' + color + '-' + degree
        hasGlass = Glass.query.filter(Glass.sku == sku).first()
        if hasGlass:
            hasGlass.amount = hasGlass.amount + int(amount)
            db.session.commit()
        else:
            newGlass = Glass(sku=sku, brand=brand, model=model, color=color, degree=degree, amount=int(amount))
            db.session.add(newGlass)
            db.session.commit()
        glasses = Glass.query.filter().all()
        operation = u'添加产品'
        content = u'添加 ' + amount + ' 个 ' + sku
        writeEmployeeLog(session.get('employee_id'), operation, content)
        return render_template('glassSKU.html', glasses = glasses)


@app.route('/eyedropSKU/', methods=['GET', 'POST'])
def eyedropSKU():
    if session.get('employee_id') is None:
        return redirect(url_for('login'))
    if request.method == 'GET':
        eyedrops = Eyedrop.query.filter().all()
        return render_template('eyedropSKU.html', eyedrops = eyedrops)
    else:
        brand = request.form.get('eyedropBrand')
        model = request.form.get('eyedropModel')
        amount = request.form.get('eyedropAmount')
        if brand == '' or model == '' or amount == '':
            eyedrops = Eyedrop.query.filter().all()
            return render_template('eyedropSKU.html', eyedrops = eyedrops)
        sku = brand + '-' + model
        hasEyedrop = Eyedrop.query.filter(Eyedrop.sku == sku).first()
        if hasEyedrop:  # 已存在
            # print(u"存在")
            hasEyedrop.amount = hasEyedrop.amount + int(amount)
            db.session.commit()
        else:   # 不存在,添加
            # print(u"不存在")
            newEyedrop = Eyedrop(sku=sku, brand=brand, model=model, amount=int(amount))
            db.session.add(newEyedrop)
            db.session.commit()
        eyedrops = Eyedrop.query.filter().all()
        operation = u'添加产品'
        content = u'添加 ' + amount + ' 个 ' + sku
        writeEmployeeLog(session.get('employee_id'), operation, content)
        return render_template('eyedropSKU.html', eyedrops = eyedrops)


@app.route('/nursingSKU/', methods=['GET', 'POST'])
def nursingSKU():
    if session.get('employee_id') is None:
        return redirect(url_for('login'))
    if request.method == 'GET':
        nursings = Nursing.query.filter().all()
        return render_template('nursingSKU.html', nursings=nursings)
    else:
        brand = request.form.get('nursingBrand')
        model = request.form.get('nursingModel')
        color = request.form.get('nursingColor')
        amount = request.form.get('nursingAmount')
        if brand == '' or model == '' or amount == '' or color == '':
            eyedrops = Eyedrop.query.filter().all()
            return render_template('nursingSKU.html', eyedrops = eyedrops)
        sku = brand + '-' + model + '-' + color
        hasNursing = Nursing.query.filter(Nursing.sku == sku).first()
        if hasNursing:  # 已存在
            # print(u"存在")
            hasNursing.amount = hasNursing.amount + int(amount)
            db.session.commit()
        else:   # 不存在,添加
            # print(u"不存在")
            newNursing = Nursing(sku=sku, brand=brand, model=model, color=color, amount=int(amount))
            db.session.add(newNursing)
            db.session.commit()
        nursings = Nursing.query.filter().all()
        operation = u'添加产品'
        content = u'添加 ' + amount + ' 个 ' + sku
        writeEmployeeLog(session.get('employee_id'), operation, content)
        return render_template('nursingSKU.html', nursings = nursings)


@app.route('/washingSKU/', methods=['GET', 'POST'])
def washingSKU():
    if session.get('employee_id') is None:
        return redirect(url_for('login'))
    if request.method == 'GET':
        washings = Washing.query.filter().all()
        return render_template('washingSKU.html', washings=washings)
    else:
        brand = request.form.get('washingBrand')
        model = request.form.get('washingModel')
        color = request.form.get('washingColor')
        amount = request.form.get('washingAmount')
        if brand == '' or model == '' or amount == '' or color == '':
            washings = Washing.query.filter().all()
            return render_template('washingSKU.html', washings=washings)
        sku = brand + '-' + model + '-' + color
        hasWashing = Washing.query.filter(Washing.sku == sku).first()
        if hasWashing:  # 已存在
            # print(u"存在")
            hasWashing.amount = hasWashing.amount + int(amount)
            db.session.commit()
        else:   # 不存在,添加
            # print(u"不存在")
            newWashing = Washing(sku=sku, brand=brand, model=model, color=color, amount=int(amount))
            db.session.add(newWashing)
            db.session.commit()
        washings = Washing.query.filter().all()
        operation = u'添加产品'
        content = u'添加 ' + amount + ' 个 ' + sku
        writeEmployeeLog(session.get('employee_id'), operation, content)
        return render_template('washingSKU.html', washings=washings)


@app.route('/sell/', methods=['GET', 'POST'])
def sell():
    buyInfo = 0
    if session.get('employee_id') is None:
        return redirect(url_for('login'))
    glasses = Glass.query.filter().all()
    eyedrops = Eyedrop.query.filter().all()
    nursings = Nursing.query.filter().all()
    washings = Washing.query.filter().all()

    if request.method == 'GET':
        return render_template('sell.html', glasses=glasses, eyedrops=eyedrops, nursings=nursings, washings=washings)
    else:
        productType = request.form.get('productType')
        price = request.form.get('price')
        if price is not '':
            price = float(price)
        amount = request.form.get('amount')
        amount = int(amount)
        cellphone = request.form.get('cellphone')
        cellphoneSearch = Customer.query.filter(Customer.cellphone == cellphone).first()
        vip = 0

        if cellphoneSearch:
            vip = cellphoneSearch.id 
        else:
            return u'手机号码不存在'
            # return render_template('sell.html', buyMsg=buyMsg, glasses=glasses, eyedrops=eyedrops, nursings=nursings, washings=washings)
        
        sku = ''
        # print(productType)
        if productType == '隐形眼镜':
            sku = request.form.get('glass_skus')
            thisSku = Glass.query.filter(Glass.sku == sku).first()
            if thisSku:
                left = thisSku.amount
                if left == 0:
                    return  u'此款无货'
                    # return render_template('sell.html', buyMsg=buyMsg, glasses=glasses, eyedrops=eyedrops, nursings=nursings, washings=washings)
                if left-int(amount) < 0:
                    return  u'库存不足,调整后再次确认.' + u'当前库存:' + str(left)
                    # return render_template('sell.html', buyMsg=msg, glasses=glasses, eyedrops=eyedrops, nursings=nursings, washings=washings)

            record = Consumption(vip=vip, sku=sku, date=datetime.datetime.now(), employeeId=session.get('employee_id'), unitPrice=price, amount=int(amount))
            db.session.add(record) # 添加
            thisSku.amount = thisSku.amount - int(amount)
            db.session.commit()

        elif productType == '眼药水':
            sku = request.form.get('eyedrop_skus')
            thisSku = Eyedrop.query.filter(Eyedrop.sku == sku).first()
            if thisSku:
                left = thisSku.amount
                if left == 0:
                    return  u'此款无货'
                    # return render_template('sell.html', buyMsg=buyMsg, glasses=glasses, eyedrops=eyedrops, nursings=nursings, washings=washings)
                if left-int(amount) < 0:
                    msg = u'库存不足,调整后再次确认.' + u'当前库存:' + str(left)
                    return msg
                    # return render_template('sell.html', buyMsg=msg, glasses=glasses, eyedrops=eyedrops, nursings=nursings, washings=washings)

            record = Consumption(vip=vip, sku=sku, employeeId=session.get('employee_id'),unitPrice=price, amount=int(amount))
            db.session.add(record) # 添加
            thisSku.amount = thisSku.amount - int(amount)
            db.session.commit()

        elif productType == '护理液':
            sku = request.form.get('nursing_skus')
            thisSku = Nursing.query.filter(Nursing.sku == sku).first()
            if thisSku:
                left = thisSku.amount
                if left == 0:
                    buyMsg = u'此款无货'
                    return buyMsg
                    # return render_template('sell.html', buyMsg=buyMsg, glasses=glasses, eyedrops=eyedrops, nursings=nursings, washings=washings)
                if left-int(amount) < 0:
                    msg = u'库存不足,调整后再次确认.' + u'当前库存:' + str(left)
                    return msg
                    # return render_template('sell.html', buyMsg=msg, glasses=glasses, eyedrops=eyedrops, nursings=nursings, washings=washings)

            record = Consumption(vip=vip, sku=sku, employeeId=session.get('employee_id'), unitPrice=price, amount=int(amount))
            db.session.add(record) # 添加
            thisSku.amount = thisSku.amount - int(amount)
            db.session.commit()
        else:
            
            sku = request.form.get('washing_skus')
            thisSku = Washing.query.filter(Washing.sku == sku).first()
            if thisSku:
                left = thisSku.amount
                if left == 0:
                    buyMsg = u'此款无货'
                    return buyMsg
                    # return render_template('sell.html', buyMsg=buyMsg, glasses=glasses, eyedrops=eyedrops, nursings=nursings, washings=washings)
                if left-int(amount) < 0:
                    msg = u'库存不足,调整后再次确认.' + u'当前库存:' + str(left)
                    return msg
                    # return render_template('sell.html', buyInfo = msg, glasses=glasses, eyedrops=eyedrops, nursings=nursings, washings=washings)
                    # return render_template('sell.html', buyMsg=msg, glasses=glasses, eyedrops=eyedrops, nursings=nursings, washings=washings)

            record = Consumption(vip=vip, sku=sku, date=datetime.datetime.now(), employeeId=session.get('employee_id'), unitPrice=price, amount=int(amount))
            db.session.add(record) # 添加
            thisSku.amount = thisSku.amount - int(amount)
            db.session.commit()

        # 更新积分和购买次数
        cellphoneSearch.purchase = cellphoneSearch.purchase + int(amount)
        thisScore = int(price * int(amount) / 20)
        cellphoneSearch.score = cellphoneSearch.score + thisScore
        db.session.commit()

        operation = u'销售'
        content = u'销售 ' + str(amount) + ' 个 ' + sku
        writeEmployeeLog(session.get('employee_id'), operation, content)
        # buyInfo = '成功'
        return render_template('sell.html',  glasses=glasses, eyedrops=eyedrops, nursings=nursings, washings=washings)


@app.route('/sellSearch/', methods=['GET', 'POST'])
def sellSearch():
    if session.get('employee_id') is None:
        return redirect(url_for('login'))
    class Item(object):
        pass
    fromDate = datetime.date.today()
    toDate = datetime.date.today()
    if request.method == 'GET':
        return render_template('sellSearch.html', fromDate=fromDate, toDate=toDate)
    else:
        total = 0
        total_glass = 0
        total_eyedrop = 0
        total_nursing = 0
        total_washing = 0

        productType = request.form.get('productType')
        startDate = request.form.get('startDate')
        endDate = request.form.get('endDate')
        if startDate == endDate and startDate == "":
            startDate = datetime.date.today()
            endDate = datetime.date.today()
            # print(startDate)
        sellRecords = Consumption.query.filter(Consumption.date >= startDate, Consumption.date <= endDate).all()
        
        items = []
        records = []
        if productType == '隐形眼镜':
            records = Glass.query.filter().all()
        elif productType == '眼药水':
            records = Eyedrop.query.filter().all()
        elif productType == '护理液':
            records = Nursing.query.filter().all()
        else:
            records = Washing.query.filter().all()

        for record in records:
            item = Item()
            item.sku = record.sku 
            item.stock = record.amount
            item.amount = 0
            item.total = 0
            for sellRecord in sellRecords:
                if item.sku == sellRecord.sku:
                    item.amount = item.amount + sellRecord.amount
                    item.total = item.total + sellRecord.amount *  sellRecord.unitPrice
            items.append(item)

        glasses = Glass.query.filter().all()
        glass_sku = [glass.sku for glass in glasses]

        eyedrops = Eyedrop.query.filter().all()
        eyedrop_sku = [eyedrop.sku for eyedrop in eyedrops]

        nursings = Nursing.query.filter().all()
        nursing_sku = [nursing.sku for nursing in nursings]

        washings = Washing.query.filter().all()
        washing_sku = [washing.sku for washing in washings]

        for sellRecord in sellRecords:
            if sellRecord.sku in glass_sku:
                total_glass += sellRecord.unitPrice * sellRecord.amount
            elif sellRecord.sku in eyedrop_sku:
                total_eyedrop += sellRecord.unitPrice * sellRecord.amount
            elif sellRecord.sku in nursing_sku:
                total_nursing += sellRecord.unitPrice * sellRecord.amount
            elif sellRecord.sku in washing_sku:
                total_washing += sellRecord.unitPrice * sellRecord.amount

        total = total_glass + total_eyedrop + total_nursing + total_washing

        return render_template('sellSearch.html', totalPrice = total, 
                                glass_totalPrice = total_glass, 
                                eyedrop_totalPrice = total_eyedrop,
                                nursing_totalPrice = total_nursing,
                                washing_totalPrice = total_washing,
                                items = items,
                                fromDate=startDate,
                                toDate=endDate)


@app.route('/personal/<employeeID>', methods=['GET', 'POST'])
def personal(employeeID):
    if session.get('employee_id') is None:
        return redirect(url_for('login'))
    msg = None
    employee_model = Employee.query.filter(Employee.id == employeeID).first()
    if request.method == 'GET':
        return render_template('personal.html', model=employee_model, employeeID=employee_model.id)
    else:
        print('OK')
        oldPassword = employee_model.password
        
        input_oldPassword = request.form.get('oldPassword')
        
        if oldPassword != input_oldPassword:
            msg =  u'旧密码错误, 更新失败'
            return msg
            # return render_template('personal.html', model=employee_model, employeeID=employee_model.id, msg=msg)
        else:
            oldCellphone = employee_model.cellphone
            oldWechat = employee_model.wechat
            oldEmail = employee_model.email

            input_cellphone = request.form.get('customerPhone')
            if oldCellphone != input_cellphone:
                temp_model = Employee.query.filter(Employee.cellphone == input_cellphone).first()
                if temp_model:
                    msg = u'手机号码已存在,更新失败'
                    return msg
                    # return render_template('personal.html', model=employee_model, employeeID=employee_model.id, msg=msg)
                else:
                    employee_model.cellphone = input_cellphone

            input_wechat = request.form.get('customerWechat')
            if oldWechat != input_wechat:
                temp_model = Employee.query.filter(Employee.wechat == input_wechat).first()
                if temp_model:
                    msg = u'微信已存在,更新失败'
                    return msg
                    # return render_template('personal.html', model=employee_model, employeeID=employee_model.id, msg=msg)
                else:
                    employee_model.wechat = input_wechat

            input_email = request.form.get('customerEmail')
            if oldEmail != input_email:
                temp_model = Employee.query.filter(Employee.email == input_email).first()
                if temp_model:
                    msg = u'邮箱已存在,更新失败'
                    return msg
                    # return render_template('personal.html', model=employee_model, employeeID=employee_model.id, msg=msg)
                else:
                    employee_model.email = input_email

            newPassword = request.form.get('newPassword')
            renewPassword = request.form.get('renewPassword')
            if newPassword == renewPassword and newPassword is not '':
                employee_model.password = newPassword
            elif newPassword != renewPassword:
                msg = u'两次密码不一致'
                return msg
                # return render_template('personal.html', model=employee_model, employeeID=employee_model.id, msg=msg)

            
            db.session.commit()
            employee_model = Employee.query.filter(Employee.id == employeeID).first()
            # msg = u'更新成功'
            # return msg
            
            return render_template('personal.html', model=employee_model, employeeID=employee_model.id)


@app.route('/outstanding/', methods=['GET', 'POST'])
def outstanding():
    if session.get('employee_id') is None:
        return redirect(url_for('login'))
    class Person(object):
        pass
    persons = []
    if request.method == 'GET':
        fromDate = datetime.date.today()
        toDate = datetime.date.today()

        return render_template('outstanding.html', fromDate=fromDate, toDate=toDate)
    else:
        startDate = request.form.get('startDate')
        endDate = request.form.get('endDate')
        cellphone = request.form.get('cellphone')
        name = ""
        employeeID = 0
        if cellphone != "":
            hasEmployee = Employee.query.filter(Employee.cellphone == cellphone).first()
            if hasEmployee:
                name = hasEmployee.name
                employeeID = hasEmployee.id
            else:
                return u'手机号码不存在'

        records = None
        if startDate == endDate and startDate == "":
            if name == "":
                records = Consumption.query.filter().all()
            else:
                records = Consumption.query.filter(Consumption.employeeId == employeeID).all()
        elif startDate != "" and endDate != "" and endDate >= startDate:
            if name == "":
                records = Consumption.query.filter(Consumption.date >= startDate, Consumption.date <= endDate).all()
            else:
                records = Consumption.query.filter(Consumption.date >= startDate, Consumption.date <= endDate, Consumption.employeeId == employeeID).all()
        else:
            return u'搜索条件错误'
        
        allEmployee = Employee.query.filter().all()
        all_employeesIds = [employee.id for employee in allEmployee if employee.duty != 'boss']
        all_employeesNames =  [employee.name for employee in allEmployee if employee.duty != 'boss']
        for  i in range(len(all_employeesIds)):
            person = Person()
            person.name = all_employeesNames[i]
            
            total = [record.unitPrice * record.amount for record in records if record.employeeId == all_employeesIds[i]]
            person.total = sum(total)
            persons.append(person)
        
        
        return render_template('outstanding.html', persons = persons, fromDate=startDate, toDate=endDate)

            
@app.route('/consumptionDetail/', methods = ['GET', 'POST'])
def consumptionDetail():
    if session.get('employee_id') is None:
        return redirect(url_for('login'))
    if request.method == 'GET':
        return render_template('consumptionDetail.html')
    else:
        class Item(object):
            pass

        cellphone = request.form.get('cellphone')
        customer = Customer.query.filter(Customer.cellphone == cellphone).first()
        if customer:
            
            customerId = customer.id
            records = Consumption.query.filter(Consumption.vip == customerId).all()
            if records:
                items = []
                for record in records:
                    item = Item()

                    customerName = customer.name
                    item.customerName = customerName

                    employeeId = record.employeeId
                    employee = Employee.query.filter(Employee.id == employeeId).first()
                    employeeName = employee.name
                    item.employeeName = employeeName
                    item.sku = record.sku
                    item.price = record.unitPrice
                    item.amount = record.amount
                    item.date = record.date

                    items.append(item)
                return render_template("consumptionDetail.html", items = items)
            else:
                return u"无消费记录"
        else:
            return u'手机号码不存在'


@app.route('/searchCustomer/', methods=['GET', 'POST'])
def searchCustomer():
    if session.get('employee_id') is None:
        return redirect(url_for('login'))
    if request.method == 'GET':
        return render_template('searchCustomer.html')
    else:
        cellphone = request.form.get('cellphone')
        hasCustomer = Customer.query.filter(Customer.cellphone == cellphone).first()
        if hasCustomer:
            persons = []
            persons.append(hasCustomer)
            return render_template('searchCustomer.html', persons = persons)
        else:
            customers = Customer.query.filter().all()
            return render_template('searchCustomer.html', persons = customers)
        return render_template('searchCustomer.html')

@app.route('/addEmployee/', methods=['GET', 'POST'])
def addEmployee():
    if session.get('employee_id') is None:
        return redirect(url_for('login'))
    if request.method == 'GET':
        return render_template('addEmployee.html')
    else:
        cellphone = request.form.get('cellphone')
        cellphone2 = request.form.get('cellphone2')
        if len(cellphone) != 11:
            return u'请输入11位手机号码'
        if cellphone != cellphone2:
            return u'手机号码输入不一致'
        employee = Employee.query.filter(Employee.cellphone == cellphone).first()
        if employee:
            return u'手机号码已存在'
        name = request.form.get('name')
        wechat = request.form.get('wechat')
        email = request.form.get('email')
        if email == "":
            email = " "
        password = request.form.get('password')
        isManager = request.form.get('isManager')
        duty = 'staff'
        if isManager:
            duty = 'manager'
        photopath = " "
        newEmployee = Employee(name=name, cellphone=cellphone,wechat=wechat, email=email, duty=duty, photopath=photopath, password=password)
        db.session.add(newEmployee)
        db.session.commit()

        operation_id = session.get('employee_id')
        operation = u'添加员工'
        content = u'新员工: ' + name
        writeEmployeeLog(operation_id, operation, content)
        return render_template('addEmployee.html')


@app.route('/searchEmployee', methods=['GET', 'POST'])
def searchEmployee():
    if session.get('employee_id') is None:
        return redirect(url_for('login'))
    class Item():
        pass
    items = []

    if request.method == 'GET':
        employees = Employee.query.filter().all()
        for employee in employees:
            item = Item()
            item.name = employee.name
            item.cellphone = employee.cellphone
            item.wechat = employee.wechat
            if employee.duty == 'boss':
                item.duty = u'老板'
                continue
            if employee.duty == 'manager':
                item.duty = u'店长'
            if employee.duty == 'staff':
                item.duty = u'员工'
            if employee.duty == 'dimission':
                item.duty = u'离职'
            items.append(item)
        return render_template('searchEmployee.html', items=items)
    else:
        cellphone = ""
        info = request.form.get('info')
        if info=="":
            employees = Employee.query.filter().all()
            for employee in employees:
                item = Item()
                item.name = employee.name
                item.cellphone = employee.cellphone
                item.wechat = employee.wechat
                if employee.duty == 'boss':
                    item.duty = u'老板'
                    continue
                if employee.duty == 'manager':
                    item.duty = u'店长'
                if employee.duty == 'staff':
                    item.duty = u'员工'
                if employee.duty == 'dimission':
                    item.duty = u'离职'
                items.append(item)
            return render_template('searchEmployee.html', items=items)
        employee = None
        if str(info).isdigit():
            cellphone = str(info)
            employee = Employee.query.filter(Employee.cellphone == cellphone).first()
        else:
            name = str(info)
            employee = Employee.query.filter(Employee.name == name).first()

        if employee:
            if employee.duty == 'boss':
                # print('exit')
                return render_template('searchEmployee.html')
            
            newDuty = request.form.get('inlineRadioOptions')

            if newDuty:
                employee.duty = newDuty
                employeeId = session.get('employee_id')
                operation = '改变员工状态'
                content = u'改为' + newDuty
                writeEmployeeLog(employeeId, operation, content)
                db.session.commit()

            item = Item()
            item.name = employee.name
            item.cellphone = employee.cellphone
            item.wechat = employee.wechat
            
            if employee.duty == 'manager':
                item.duty = u'店长'
            if employee.duty == 'staff':
                item.duty = u'员工'
            if employee.duty == 'dimission':
                item.duty = u'离职'
            items.append(item)
            return render_template('searchEmployee.html', items = items)
        else:
            return render_template('searchEmployee.html')



@app.route('/selfSearch/', methods=['GET', 'POST'])
def selfSearch():
    if request.method == 'GET':
        return render_template('selfSearch.html')
    else:
        cellphone = request.form.get('cellphone')
        customer = Customer.query.filter(Customer.cellphone == cellphone).first()
        if customer:
            session['customer_id'] = customer.id
            return redirect(url_for('selfSearchResult'))
        else:
            return u'您好,您查询的会员信息不存在'
    

@app.route('/selfSearchResult/', methods=['GET', 'POST'])
def selfSearchResult():
    if session.get('customer_id') is None:
        return redirect(url_for('selfSearch'))
    if request.method == 'GET':
        customerId = session.get('customer_id')
        customer = Customer.query.filter(Customer.id == customerId).first()
        lastName = str(customer.name)[0]
        firstName = "*" * (len(str(customer.name))-1)
        name = lastName + firstName
        cellphone = customer.cellphone
        tail = cellphone[-4:]
        return render_template('selfSearchResult.html', customer = customer, name = name, tail = tail)
        
            
    else:
        if session.get('customer_id'):
            session.pop('customer_id')
        return redirect(url_for('selfSearch')) 
        



        

@app.context_processor
def my_context_processor():
    employee_id = session.get('employee_id')
    if employee_id:
        employee = Employee.query.filter(Employee.id == employee_id).first()
        # print(employee.name)
        if employee:
            return {'employee': employee}
    return {}


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)