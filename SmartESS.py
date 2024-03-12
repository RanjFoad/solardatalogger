import requests
import json
import hashlib
import datetime
import time

class UserInfo:
    uid = ""
    usr = ""
    role = ""
    email = ""
    bomb = ""
    enable = ""
    gts = ""
    lastAtuhTs = ""
    lastAtuhAddr = ""
    emailAccr = ""
    mobileAccr = ""
    chartStatus = ""
    prompt = ""

class DeviceStatus:
    bt_status=None
    pv_status=None
    gd_status = None
    bc_status=None
    ol_status=None
    we_status=None
    mi_status=None
    total_energy=0
    updatetime=datetime.datetime.now()

class InfoItem:
    Title=""
    Value=""
    Unit=""

class BatteryStatus:
    capacity=InfoItem()
    voltage=InfoItem()
    chargingcurrent=InfoItem()
    dischargecurent=InfoItem()

class SolarPvStatus:
    power=InfoItem()
    current=InfoItem()
    voltage=InfoItem()

class GridStatus:
    voltage=InfoItem()
    freq=InfoItem()

class Usage:
    activepower=InfoItem()
    voltage=InfoItem()
    freq=InfoItem()
    load=InfoItem()

class SmartESS:
    secret = ""
    token = ""
    lasterror = ""
    tokenexpire = datetime.datetime.now()

    user =""
    password =""
    companykey = "bnrl_frRFjEz8Mkn"
    devices=[]
    userinfo=UserInfo()

    def __init__(self, user, password):
        self.user=user
        self.password=password

    def __findvalue(self,data,par):
        for item in data:
            if item["par"]==par:
                if "unit"  not in item:
                    tmpunit=""
                else:
                    tmpunit = item["unit"]
                return {"val":item["val"],"unit":tmpunit,"status":item["status"]}

    def __finditem(self,data,par)->InfoItem:
        tmpitem=InfoItem()
        for item in data:
            if item["title"]==par:
                tmpitem.Title=par
                tmpitem.Unit=item["unit"]
                tmpitem.Value=item["val"]
                return  tmpitem
        return None

    def get_salt(self):
        return str(int(time.mktime(datetime.datetime.now().utctimetuple()) * 1000))
    def authenticate(self):
        return self.__auth(self.user, self.password, self.companykey)

    def __auth(self,username, password, companykey):

        salt = self.get_salt()

        # SHA-1(salt + SHA-1(pwd) + "&action=auth&usr=" + usr + "&company-key=" + company-key);
        hash = hashlib.sha1(password.encode())
        beforefinal = (
                    salt + hash.hexdigest() + "&action=authSource&usr=" + username + "&company-key=" + companykey + "&source=1&lang=en_US")
        hash2 = hashlib.sha1(beforefinal.encode())
        sign = hash2.hexdigest()
        url = "http://android.shinemonitor.com/public/?sign={}&salt={}&action=authSource&usr={}&company-key={}&source=1&lang=en_US".format(
            sign, salt, username, companykey)
        # print(url)
        x = requests.get(url)
        Data = json.loads(x.text)
        if (Data["desc"] == "ERR_NONE"):
            self.secret = Data["dat"]["secret"]
            self.token = Data["dat"]["token"]
            self.lasterror = ""
            self.tokenexpire = datetime.datetime.now() + datetime.timedelta(seconds=int(Data["dat"]["expire"]))
            return True
        else:
            lasterror = Data["desc"]
            return False

    def  getaction(self,action):
        salt = self.get_salt()
        beforefinal = (salt + self.secret + self.token + "&" + action)
        hash2 = hashlib.sha1(beforefinal.encode())
        sign = hash2.hexdigest()
        url = "http://android.shinemonitor.com/public/?sign={}&salt={}&token={}&{}".format(sign, salt, self.token, action)
        x = requests.get(url)
        Data = json.loads(x.text)
        if (Data["desc"] == "ERR_NONE"):
            self.lasterror = ""
            return Data
        else:
            self.lasterror = Data["desc"]

    def getdevicesupdate(self):
       result= self.getaction("action=webQueryDeviceEs&devtype=2304&page=0&pagesize=10&orderBy=ascalias&i18n=en_US&lang=en_US&source=1")
       if(result["err"]==0):
           numberdevice=result["dat"]["total"]
           if(numberdevice>0):
               for i in range(numberdevice):
                   device=Device()
                   device.devalias = result["dat"]["device"][i]["devalias"]
                   device.sn = result["dat"]["device"][i]["sn"]
                   device.status = result["dat"]["device"][i]["status"]
                   device.brand = result["dat"]["device"][i]["brand"]
                   device.devtype = result["dat"]["device"][i]["devtype"]
                   device.collalias = result["dat"]["device"][i]["collalias"]
                   device.pn = result["dat"]["device"][i]["pn"]
                   device.devaddr = result["dat"]["device"][i]["devaddr"]
                   device.devcode = result["dat"]["device"][i]["devcode"]
                   device.usr = result["dat"]["device"][i]["usr"]
                   device.uid = result["dat"]["device"][i]["uid"]
                   device.profitToday = result["dat"]["device"][i]["profitToday"]
                   device.profitTotal = result["dat"]["device"][i]["profitTotal"]
                   device.buyProfitToday = result["dat"]["device"][i]["buyProfitToday"]
                   device.buyProfitTotal = result["dat"]["device"][i]["buyProfitTotal"]
                   device.sellProfitToday = result["dat"]["device"][i]["sellProfitToday"]
                   device.sellProfitTotal = result["dat"]["device"][i]["sellProfitTotal"]
                   device.pid = result["dat"]["device"][i]["pid"]
                   device.focus = result["dat"]["device"][i]["focus"]
                   device.outpower = result["dat"]["device"][i]["outpower"]
                   device.energyToday = result["dat"]["device"][i]["energyToday"]
                   device.energyYear = result["dat"]["device"][i]["energyYear"]
                   device.energyTotal = result["dat"]["device"][i]["energyTotal"]
                   device.buyEnergyToday = result["dat"]["device"][i]["buyEnergyToday"]
                   device.buyEnergyTotal = result["dat"]["device"][i]["buyEnergyTotal"]
                   device.sellEnergyToday = result["dat"]["device"][i]["sellEnergyToday"]
                   device.sellEnergyTotal = result["dat"]["device"][i]["sellEnergyTotal"]
                   self.devices.append(device)
           return True
       else:
           return False

    def getaccountinfo(self):
        result= self.getaction("action=queryAccountInfo&i18n=en_US&lang=en_US&source=1")
        if (result["err"] == 0):
            self.userinfo.uid = result["dat"]["uid"]
            self.userinfo.usr = result["dat"]["usr"]
            self.userinfo.role = result["dat"]["role"]
            self.userinfo.email = result["dat"]["email"]
            self.userinfo.bomb = result["dat"]["bomb"]
            self.userinfo.enable = result["dat"]["enable"]
            self.userinfo.gts = result["dat"]["gts"]
            self.userinfo.lastAtuhTs = result["dat"]["lastAtuhTs"]
            self.userinfo.lastAtuhAddr = result["dat"]["lastAtuhAddr"]
            self.userinfo.emailAccr = result["dat"]["emailAccr"]
            self.userinfo.mobileAccr = result["dat"]["mobileAccr"]
            self.userinfo.chartStatus = result["dat"]["chartStatus"]
            self.userinfo.prompt = result["dat"]["prompt"]
            return True
        else:
            return False

    def renewtoken(self):
        result = self.getaction("action=updateToken&lang=en_U&source=1")
        if (result is not None and result["err"] == 0):
            self.secret = result["dat"]["secret"]
            self.token = result["dat"]["token"]
            self.lasterror = ""
            self.tokenexpire = datetime.datetime.now() + datetime.timedelta(seconds=int(result["dat"]["expire"]))
            return True
        else:
            if (result is not None):
                self.lasterror = result["desc"]
            else:
                self.lasterror = "Unknown error."
            return False

    def getdeviceenergyflow(self,devicepin, serialnumber, deviceaddress, devicecode):
        result= self.getaction(
            "action=webQueryDeviceEnergyFlowEs&pn={}&sn={}&devaddr={}&devcode={}&i18n=en_US&lang=en_US&source=1".format(
                devicepin, serialnumber, deviceaddress, devicecode))
        if result["err"]==0:
            devicestatus=DeviceStatus()
            devicestatus.brand=result["dat"]["brand"]
            devicestatus.status=result["dat"]["status"]
            if result["dat"]["bt_status"]!=None:
                devicestatus.bt_status=BatteryStatus()
                tmp=self.__findvalue(result["dat"]["bt_status"],"bt_battery_capacity")
                devicestatus.bt_status.capacity=float(tmp["val"])
                devicestatus.bt_status.capstatus=tmp["status"]
                tmp = self.__findvalue(result["dat"]["bt_status"], "battery_active_power")
                devicestatus.bt_status.activepower=float(tmp["val"])
                devicestatus.bt_status.apstatus=tmp["status"]
            if result["dat"]["pv_status"]!=None:
                devicestatus.pv_status=SolarPvStatus()
                tmp=self.__findvalue(result["dat"]["pv_status"],"pv_output_power")
                devicestatus.pv_status.pvpower=float(tmp["val"])
                devicestatus.pv_status.status=tmp["status"]
            if result["dat"]["gd_status"]!=None:
                devicestatus.gd_status=GridStatus()
                tmp=self.__findvalue(result["dat"]["gd_status"],"grid_active_power")
                devicestatus.gd_status.activepower=float(tmp["val"])
                devicestatus.gd_status.status=tmp["status"]
            if result["dat"]["bc_status"]!=None:
                devicestatus.bc_status=GridStatus()
                tmp=self.__findvalue(result["dat"]["bc_status"],"load_active_power")
                devicestatus.bc_status.activepower=float(tmp["val"])
                devicestatus.bc_status.status=tmp["status"]
        return devicestatus

    def getdevicestatus(self,devid)->DeviceStatus:
        devicepin=self.devices[devid].pn
        serialnumber=self.devices[devid].sn
        deviceaddress=self.devices[devid].devaddr
        devicecode=self.devices[devid].devcode
        result= self.getaction(
            "action=queryDeviceLastData&pn={}&sn={}&devaddr={}&devcode={}&i18n=en_US&lang=en_US&source=1".format(
                devicepin, serialnumber, deviceaddress, devicecode))
        if result["err"]==0:
            tmpdat=result["dat"]
            devicestatus=DeviceStatus()
            devicestatus.bt_status=BatteryStatus()
            devicestatus.pv_status=SolarPvStatus()
            devicestatus.gd_status=GridStatus()
            devicestatus.bc_status=Usage()

            devicestatus.bt_status.capstatus = self.__finditem(tmpdat,"Battery capacity")
            devicestatus.bt_status.voltage = self.__finditem(tmpdat, "Battery voltage")
            devicestatus.bt_status.chargingcurrent = self.__finditem(tmpdat, "Battery charging current")
            devicestatus.bt_status.dischargecurent = self.__finditem(tmpdat, "Battery discharge current")

            devicestatus.pv_status.voltage = self.__finditem(tmpdat, "PV Input voltage")
            devicestatus.pv_status.power = self.__finditem(tmpdat, "PV Charging power")
            devicestatus.pv_status.current = self.__finditem(tmpdat, "PV Input current for battery")

            devicestatus.gd_status.voltage = self.__finditem(tmpdat, "Grid voltage")
            devicestatus.gd_status.freq = self.__finditem(tmpdat, "Grid frequency")

            devicestatus.bc_status.freq = self.__finditem(tmpdat, "AC output frequency")
            devicestatus.bc_status.activepower = self.__finditem(tmpdat, "AC output active power")
            devicestatus.bc_status.voltage = self.__finditem(tmpdat, "AC output voltage")
            devicestatus.bc_status.load = self.__finditem(tmpdat, "Output load percent")
            result = self.getaction(
            "action=queryDeviceLastData&pn={}&sn={}&devaddr={}&devcode={}&i18n=en_US&lang=en_US&source=1".format(
                devicepin, serialnumber, deviceaddress, devicecode))
        result = self.getaction(
            "action=webQueryDeviceEs&pn={}&sn={}&devaddr={}&devcode={}&i18n=en_US&lang=en_US&source=1".format(
                devicepin, serialnumber, deviceaddress, devicecode
            )
        )

        if result["err"] == 0:
            devicestatus.total_energy = float(result["dat"]["device"][0]["energyTotal"])

        return devicestatus



class Device:
    devalias = ""
    sn = ""
    status = ""
    brand = ""
    devtype = ""
    collalias = ""
    pn = ""
    devaddr = ""
    devcode = ""
    usr = ""
    uid = ""
    profitToday = ""
    profitTotal = ""
    buyProfitToday = ""
    buyProfitTotal = ""
    sellProfitToday = ""
    sellProfitTotal = ""
    pid = ""
    focus = ""
    outpower = ""
    energyToday = ""
    energyYear = ""
    energyTotal = ""
    buyEnergyToday = ""
    buyEnergyTotal = ""
    sellEnergyToday = ""
    sellEnergyTotal = ""

