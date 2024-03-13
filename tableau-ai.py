import tableauserverclient as TSC
from tableau_api_lib import TableauServerConnection

# server authentication
tableau_auth = TSC.TableauAuth('sohampatil.ai@gmail.com', 'Soham123@', site_id='sohampatilai5401868afb')
server = TSC.Server('https://prod-useast-b.online.tableau.com')
#server.auth.sign_in(tableau_auth)

with server.auth.sign_in(tableau_auth):
    file_path = server.workbooks.download('2ba55752-f776-4214-8021-7b23440a7967')
    print("\nDownloaded the file to {0}.".format(file_path))
    
    
    # wb_item = TSC.WorkbookItem(name='NewWB', project_id='552af7a2-b16c-4ce4-97e4-29538dce452b')
    # # call the publish method with the workbook item
    # workbook_file_path = '/Users/soham/Downloads/wbwb.twbx'
    # wb_item = server.workbooks.publish(wb_item, workbook_file_path, 'Overwrite')
    
    
    # all_workbooks_items, pagination_item = server.workbooks.get()
    
    # # Print the IDs and names of the first 100 workbooks
    # print([workbook.id for workbook in all_workbooks_items])
    # print([workbook.name for workbook in all_workbooks_items])


