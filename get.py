import obtain
from initialize import loc
from initialize import create
import data_request
import inspect
import auto

# Updated with SDI v1.2

def GET():
    current_processes = str(inspect.getouterframes(inspect.currentframe(), 2))
    automated = True if "auto.py" in current_processes else False
    if automated:
        print("get.py is being ran as a subprocess of auto.py")
        request_check = getting[0]
        unpack_check = getting[1]
        check = getting[2]
        download_location = getting[3]
    if not automated: request_check = raw_input("-> Get data from LCO or unpack downloaded data? (dl/unpack) (leave blank for default = unpack): ")
    if request_check == 'dl':
        data_request.request()
        if not automated: unpack_check = raw_input("-> Unpack downloaded data? (y/n) (leave blank for default = y): ")
        if ((unpack_check == 'y') or (unpack_check == '')):
            obtain.move(loc+'/sdi/temp')
            obtain.process()
            if not automated: check = raw_input("-> Move data into target directory? (y/n) (leave blank for default = y): ")
            if ((check == "y") or (check == "")):
                try:
                    obtain.movetar()
                except UnboundLocalError:
                    print("-> No data in 'temp' to move")
                obtain.rename()
            elif ((check != "y" and check != "") and (check != "n")):
                print("-> Error: unknown Input")
    elif ((request_check == 'unpack') or (request_check == '')):
        if not automated: download_location = raw_input("-> Enter LCO data location (leave blank for default=%s/Downloads): " % (loc))
        if download_location == "":
            download_location = "%s/Downloads" % (loc)
        obtain.move(download_location)
        obtain.process()
        if not automated: check = raw_input("-> Move data into target directory? (y/n) (leave blank for default = y): ")
        if ((check == "y") or (check == "")):
            try:
                obtain.movetar()
            except UnboundLocalError:
                print("-> No data in 'temp' to move")
            obtain.rename()
        elif ((check != "y" and check != "") and (check != "n")):
            print("-> Error: unknown Input")

if __name__ == '__main__':
    current_processes = str(inspect.getouterframes(inspect.currentframe(), 2))
    automated = True if "auto.py" in current_processes else False
    if automated:
        print("get.py is being ran as a subprocess of auto.py")
        request_check = getting[0]
        unpack_check = getting[1]
        check = getting[2]
        download_location = getting[3]
    if not automated: request_check = raw_input("-> Get data from LCO or unpack downloaded data? (dl/unpack) (leave blank for default = unpack): ")
    if request_check == 'dl':
        data_request.request()
        if not automated: unpack_check = raw_input("-> Unpack downloaded data? (y/n) (leave blank for default = y): ")
        if ((unpack_check == 'y') or (unpack_check == '')):
            obtain.move(loc+'/sdi/temp')
            obtain.process()
            if not automated: check = raw_input("-> Move data into target directory? (y/n) (leave blank for default = y): ")
            if ((check == "y") or (check == "")):
                try:
                    obtain.movetar()
                except UnboundLocalError:
                    print("-> No data in 'temp' to move")
                obtain.rename()
            elif ((check != "y" and check != "") and (check != "n")):
                print("-> Error: unknown Input")
    elif ((request_check == 'unpack') or (request_check == '')):
        if not automated: download_location = raw_input("-> Enter LCO data location (leave blank for default=%s/Downloads): " % (loc))
        if download_location == "":
            download_location = "%s/Downloads" % (loc)
        obtain.move(download_location)
        obtain.process()
        if not automated: check = raw_input("-> Move data into target directory? (y/n) (leave blank for default = y): ")
        if ((check == "y") or (check == "")):
            try:
                obtain.movetar()
            except UnboundLocalError:
                print("-> No data in 'temp' to move")
            obtain.rename()
        elif ((check != "y" and check != "") and (check != "n")):
            print("-> Error: unknown Input")