from drive import MyDrive, file_types
import io


class DriveApi(MyDrive):
    def get_all(self, folder_name):
        parent = self.check_folder(folder_name)
        if parent == False:
            return 'Folder not found'
        return self.list_folder(parent)

    def get(self, id):
        obj = {
            'json': '',
            'image': ''
        }
        files = self.list_folder(id)
        print(files)
        for file in files:
            file_id = file['id']
            if file['type'] == file_types['json']:
                json = self.get_json(file_id)
                obj['json'] = json
            if file['type'] == file_types['image']:
                obj['image'] = file_id
        print(obj)
        return obj

    def create(self, files, folder_name):
        parent = self.check_folder(folder_name)
        if not parent:
            parent = self.create_folder(folder_name)
        folder_id = self.create_folder('rocket', parent)
        for file in files:
            self.create_file(file['file'], file['mimeType'], folder_id)
        return folder_id

    def update(self, data, folder_id):
        folder = self.check_folder_by_id(folder_id)
        if folder == False:
            return 'folder not found'
        files = self.list_folder(folder_id)
        print(files)
        for file in files:
            file_id = file['id']
            if file['type'] == file_types['json']:
                try:
                    self.update_file(file_id, data['json'])
                except:
                    print('not found json')
            if file['type'] == file_types['image']:
                try:
                    self.update_file(file_id, data['image'])
                except:
                    print('not found image')
        return 'updated'

    def delete(self, id):
        pass

def main():
    my_drive = DriveApi()
    # print(my_drive.get_file('1YUNp3m-VEm0IcOJJ8-2EbZI0YWVS3UXd'))
    # file = io.BytesIO(b'asdasd')
    # my_drive.create_file(file)
    my_drive.get_all('projects')
    my_drive.get('1x-B_D8MyZEEVr8qLbHUx8fpmcvE2eNiI')
    file = {
        'file': io.StringIO('asdasdasd'),
        'mimeType': 'application/json'
    }
    my_drive.create([file], 'new')
    

if __name__ == '__main__':
    main()
