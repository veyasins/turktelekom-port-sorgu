import requests
import bs4
import json
from email.message import EmailMessage
import time
from datetime import datetime
import smtplib
bbk = "0000000000" #buraya goknet.com.tr port sorgu sayfasina adresinizi girince cikan kodu yapistirin

url = "https://user.goknet.com.tr/sistem/getTTAddressWebservice.php?kod="+str(bbk)+"&datatype=checkAddress"

while True:
    time.sleep(60)
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")

    try:
        page = requests.get(url)
        soup = bs4.BeautifulSoup(page.text, 'html.parser')
        data = json.loads(str(soup))

        deger = data['6']['flexList']['flexList'][2]['value'] #portun 1 veya 0 cinsinden değeri
        hatakod = data['6']['hataKod'] #hata kodu
        mesaj = data['6']['hataMesaj'] #sorgulama sonucu cikan mesaj

        if deger == '1':
            portdurumu = 'VAR'
        else:
            portdurumu = 'YOK'    

        #Burada port degeri 1 (port var) oldugunda size haber icin bir mail gonderecek
        msg= EmailMessage()
        my_address ="gonderen@gonderen.com"    #gonderenin e mail adresi (kendi adresiniz)
        app_generated_password = "gmailuygulamasifreniz"    #gmailde olusturdugunuz uygulamaya ozel sifre
        msg["Subject"] = "TT Port Bilgilendirme"   #mailin konusu 
        msg["From"]= my_address      #gonderen (burayi degistirmeyin)
        msg["To"] = "alici@alici.com"     #alici adres(mailin gidecegi kisi)
        msg.set_content(mesaj+" Port durumu: "+portdurumu+" Hata kodu: "+hatakod)   #mailin icerigi

        if deger == '1':
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                smtp.login(my_address,app_generated_password)    #mail hesabina giris yapiyor
                smtp.send_message(msg)   #mail gonderildi             
                print('['+current_time+'] Port Durumu: '+portdurumu+' Mail gonderildi.')
        else:
                print('['+current_time+'] Port Durumu: '+portdurumu)
    except:
          print("Bir hata meydana geldi")
