import os
import urllib.request
import zipfile
import shutil

import logging
logging.basicConfig(filename='error.log', format='%(asctime)s - %(levelname)s - %(message)s', level=logging.DEBUG)

class NetworkManager():
    def __init__(self):
        self.tempfolder = ""

    def InstallFile(self,url,download_path,path,filename):
        logging.debug(f"NETWORK - downloading file '{url}'")
        try:

            os.makedirs(download_path, exist_ok=True)
            try:

                urllib.request.urlretrieve(url,os.path.join(download_path,filename))
                shutil.move(os.path.join(download_path,filename),os.path.join(path,filename))
                
            except Exception as a:
                self.ErrorMessageBox(f"NetworkError: {a}")
                return False
            return True
        except Exception as e:
            self.ErrorMessageBox(f"UnexpectedError: {e}")
            return False
        return True
    def InstallZip(self,url,download_path,extract_path):
        logging.debug(f"NETWORK - downloading zip '{url}'")
        try:
 

            if os.path.exists(download_path):
                try:
                    os.remove(download_path)
                except Exception as e:
                    self.ErrorMessageBox(f"141: Error deleting existing zip: {e}")
            try:
                urllib.request.urlretrieve(url, download_path)
            except Exception as e:
                self.ErrorMessageBox(f"ERROR - download error: {e} {url}")
                return False
            try:
                with zipfile.ZipFile(download_path, 'r') as zip_ref:
                    zip_ref.extractall(extract_path)

            except zipfile.BadZipFile as e:
                self.ErrorMessageBox(f"ERROR - extraction failed due to bad zip file - {e}")
                return False
            except Exception as e:
                self.ErrorMessageBox(f"ERROR - extraction failed due to {e}")
                return False
            try:
                os.remove(download_path)
            except Exception as e:
                self.ErrorMessageBox(f"ERROR - failed to delete zip after use {e}")
                return True
        except Exception as e:
            self.ErrorMessageBox(f"ERROR - an unexpected error occured {e}")
            return False
    def ErrorMessageBox(self,string):
        logging.error(string)
    