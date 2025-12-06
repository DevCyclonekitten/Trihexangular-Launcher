import os
import urllib.request
import zipfile
import shutil


class NetworkManager():
    def __init__(self):
        self.tempfolder = ""

    def InstallFile(self,url,download_path,path,filename):
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
        try:
 

            if os.path.exists(download_path):
                try:
                    os.remove(download_path)
                except Exception as e:
                    self.ErrorMessageBox(f"141: Error deleting existing zip: {e}")
            try:
                urllib.request.urlretrieve(url, download_path)
            except Exception as e:
                self.ErrorMessageBox(f" 146: Download Error: {e}")
                return False
            try:
                with zipfile.ZipFile(download_path, 'r') as zip_ref:
                    zip_ref.extractall(extract_path)

            except zipfile.BadZipFile as e:
                self.ErrorMessageBox(f"152: Extraction failed: Invalid zip file - {e}")
                return False
            except Exception as e:
                self.ErrorMessageBox(f"155: Extraction failed with an unexpected error: {e}")
                return False
            try:
                os.remove(download_path)
            except Exception as e:
                self.ErrorMessageBox(f"160: Error deleting zip after extraction: {e}")
                return True
        except Exception as e:
            self.ErrorMessageBox(f"163: An unexpected error occurred: {e}")
            return False
    def ErrorMessageBox(self,string):
        print(string)
    