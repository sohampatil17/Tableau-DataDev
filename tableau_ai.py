import zipfile, os, shutil
import tableauserverclient as TSC
from tableau_api_lib import TableauServerConnection
import csv

chart_type_to_url = {
    "piechart": "https://prod-useast-b.online.tableau.com/t/sohampatilai5401868afb/authoring/piechart_workbook/Sheet1#1",
    "bargraph": "https://prod-useast-b.online.tableau.com/t/sohampatilai5401868afb/authoring/bargraph_workbook/Sheet1#1",
    "bubbles": "https://prod-useast-b.online.tableau.com/t/sohampatilai5401868afb/authoring/bubbles_workbook/Sheet1#1",
    "map": "https://prod-useast-b.online.tableau.com/t/sohampatilai5401868afb/authoring/map_workbook/Sheet1#1",
    "linegraph": "https://prod-useast-b.online.tableau.com/t/sohampatilai5401868afb/authoring/linegraph_workbook/Sheet1#1"
}

def update_tableau_workbook(csv_content, workbook_id, chart_type):
    # Save the CSV content to a file
    csv_file_path = 'data_source.csv'
    with open(csv_file_path, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        for line in csv_content:
            cleaned_line = line.replace("```","").strip()
            if cleaned_line:
                csvwriter.writerow(cleaned_line.split(','))

    # Authenticate with the Tableau server
    tableau_auth = TSC.TableauAuth('sohampatil.ai@gmail.com', 'Soham123@', site_id='sohampatilai5401868afb')
    server = TSC.Server('https://prod-useast-b.online.tableau.com')

    with server.auth.sign_in(tableau_auth):
        # Download the workbook
        file_path = server.workbooks.download(workbook_id)

        # Extract the workbook content
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall('extracted_workbook')
        
    # Replacing every data source CSV in the extracted folder
    for root, dirs, files in os.walk('extracted_workbook'):
        for file in files:
            if file.endswith('.csv'):  # Check if the file is a CSV
                target_csv = os.path.join(root, file)
                shutil.copy2(csv_file_path, target_csv)

    # Repackage the workbook
    new_workbook_path = 'repacked_workbook.twbx'
    with zipfile.ZipFile(new_workbook_path, 'w') as zipf:
        for root, dirs, files in os.walk('extracted_workbook'):
            for file in files:
                file_path = os.path.join(root, file)
                archive_path = os.path.relpath(file_path, 'extracted_workbook')
                zipf.write(file_path, archive_path)

    # Publish the modified workbook
    with server.auth.sign_in(tableau_auth):
        workbook_name = f"{chart_type}_workbook"
        new_workbook = TSC.WorkbookItem(name=workbook_name, project_id='f482dbe9-85a6-487a-814b-98bedb08647f')
        published_workbook = server.workbooks.publish(new_workbook, new_workbook_path, 'Overwrite')

        # Construct the URL to view the updated workbook
        # Modify this based on how you want to generate/view the URL
        workb_url = f"https://prod-useast-b.online.tableau.com/t/sohampatilai5401868afb/authoring/{published_workbook.id}/Sheet1#1"
    
    return chart_type_to_url[chart_type]




# # Authenticate with the Tableau server
# tableau_auth = TSC.TableauAuth('sohampatil.ai@gmail.com', 'Soham123@', site_id='sohampatilai5401868afb')
# server = TSC.Server('https://prod-useast-b.online.tableau.com')

# with server.auth.sign_in(tableau_auth):
#     # Download the workbook
#     file_path = server.workbooks.download('0fcf1b3b-1c77-4f54-8e2f-c9d135e60265')
#     print(f"\nDownloaded the file to {file_path}.")

#     # Extract the workbook content
#     with zipfile.ZipFile(file_path, 'r') as zip_ref:
#         zip_ref.extractall('extracted_workbook')
#         print("Extracted the workbook.")
        
        
# # Replacing every data source csv in the extracted folder
# root_csv = 'data_source.csv'

# for root, dirs, files in os.walk('extracted_workbook'):
#     for file in files:
#         if file.endswith('.csv'):  # Check if the file is a CSV
#             target_csv = os.path.join(root, file)
#             shutil.copy2(root_csv, target_csv)
#             print(f"Replaced {target_csv} with {root_csv}")

# # After manual changes, repackage the workbook
# new_workbook_path = 'repacked_workbook.twbx'
# with zipfile.ZipFile(new_workbook_path, 'w') as zipf:
#     for root, dirs, files in os.walk('extracted_workbook'):
#         for file in files:
#             file_path = os.path.join(root, file)
#             archive_path = os.path.relpath(file_path, 'extracted_workbook')
#             zipf.write(file_path, archive_path)
# print(f"Repackaged workbook saved to {new_workbook_path}")

# # def get_workbook_view_url(server, workbook_id):
# #     server.workbooks.populate_views(workbook_id)
# #     views = workbook_id.views
# #     if views:
# #         # Assuming you want to link to the first view in the workbook
# #         first_view = views[0]
# #         return f"https://{server.server}/#/site/{server.site_id}/workbooks/{workbook_id.id}/views/{first_view.id}"
# #     else:
# #         return "No views available in this workbook."
    
# # Publish the modified workbook
# with server.auth.sign_in(tableau_auth):
#     new_workbook = TSC.WorkbookItem(name='soham_workbook', project_id='f482dbe9-85a6-487a-814b-98bedb08647f')
#     published_workbook = server.workbooks.publish(new_workbook, new_workbook_path, 'Overwrite')
#     print("Publishing workbook")
#     workbook_url = "https://prod-useast-b.online.tableau.com/t/sohampatilai5401868afb/authoring/soham_workbook/Sheet1#1"
#     print(f"Workbook published. You can view it at: {workbook_url}")

#     # workbook_view_url = get_workbook_view_url(server, published_workbook)
#     # print(f"View the workbook at: {workbook_view_url}")

# # # Finding workbook IDs and Project IDs

# # with server.auth.sign_in(tableau_auth):
# #     all_workbooks_items, pagination_item = server.workbooks.get()
    
# #     # Print the IDs, names, and project IDs of the workbooks
# #     for workbook in all_workbooks_items:
# #         print(f"Workbook ID: {workbook.id}, Workbook Name: {workbook.name}, Project ID: {workbook.project_id}")

