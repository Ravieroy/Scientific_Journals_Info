import pandas as pd

# from pandas import read_csv
import tkinter as tk
import requests
from tkinter import messagebox

HEIGHT = 700
WIDTH = 800

# ------Formats the response to be shown ----------


def format_response(search_results):
    journal_name = search_results.iloc[0]["Title"]
    country_name = search_results.iloc[0]["Country"]
    rank = search_results.iloc[0]["Rank"]
    sjr = search_results.iloc[0]["SJR"]
    h_index = search_results.iloc[0]["H index"]
    total_docs_in_three = search_results.iloc[0]["Total Docs. (3years)"]
    total_cites_in_three = search_results.iloc[0]["Total Cites (3years)"]
    citation_per_doc = search_results.iloc[0]["Cites / Doc. (2years)"]
    categories = search_results.iloc[0]["Categories"]

    # The following is because sometimes the number of items in categories is too many and goes beyond the box
    categories_list = categories.split(";")
    joined_list = "\n".join(categories_list)

    final_string = """Journal Name: %s \nCountry: %s \nRank: %s \nSJR: %s \nH-Index: %s \nTotal Docs(3Y): %s \nTotal Citations(3Y): %s \nCitations per Doc(2Y):  %s \nCategories: %s
    """ % (
        journal_name,
        country_name,
        rank,
        sjr,
        h_index,
        total_docs_in_three,
        total_cites_in_three,
        citation_per_doc,
        joined_list,
    )

    return final_string


# -----Gets the data in the csv format and returns meaningful values----


def get_data(journal_name):
    if journal_name != "":  # This if block checks if the entry field is empty.
        try:
            fileName = "journal_database.csv"
            try:
                data = pd.read_csv(
                    fileName, sep=";", index_col=False, dtype="object"
                )  # Read csv data
                list_of_items = [
                    "Rank",
                    "Sourceid",
                    "Title",
                    "SJR",
                    "H index",
                    "Total Docs. (3years)",
                    "Total Cites (3years)",
                    "Cites / Doc. (2years)",
                    "Country",
                    "Publisher",
                    "Categories",
                ]
                data = data[list_of_items]
                search_results = data.loc[
                    data["Title"].str.contains(journal_name, case=False)
                ]
                label["text"] = format_response(search_results)
                return search_results
            except FileNotFoundError:
                messagebox.showerror(
                    "FileNotFoundError",
                    "journal_databse.csv not found. Press Update DB button",
                )

        except IndexError:
            messagebox.showerror("Name Error", "Please enter a valid name")
    else:
        messagebox.showerror("Empty String", "The Entry can not be empty")


# -------Searches through the database for possible hits and shows in the search box----


def search_command(journal_name):

    if journal_name != "":  # This if block checks if the entry field is empty.

        fileName = "journal_database.csv"
        try:
            data = pd.read_csv(
                fileName, sep=";", index_col=False, dtype="object"
            )  # Read csv data

            list_of_items = [
                "Rank",
                "Sourceid",
                "Title",
                "SJR",
                "H index",
                "Total Docs. (3years)",
                "Total Cites (3years)",
                "Country",
                "Publisher",
                "Categories",
            ]
            data = data[list_of_items]

            search_results = data.loc[
                data["Title"].str.contains(journal_name, case=False)
            ]
            journal_name_list = []
            for journal_names in range(len(search_results)):
                journal_name_list.append(search_results.iloc[journal_names]["Title"])

            Str = "\n".join(journal_name_list)
            text = tk.Text(label_bottom)
            text.place(relwidth=1, relheight=1)
            text.insert(tk.END, Str)

        except FileNotFoundError:
            messagebox.showerror(
                "FileNotFoundError",
                "journal_databse.csv not found. Press Update DB button",
            )

    else:
        messagebox.showerror("Empty String", "The Entry can not be empty")


def update_command():  # This will download the csv file if not already present. If it is present it will overwrite it
    try:
        download_url = "https://www.scimagojr.com/journalrank.php?out=xls"
        requests.get(download_url)
        r = requests.get(download_url, allow_redirects=True)
        open("journal_database.csv", "wb").write(r.content)
        messagebox.showinfo("Update", "Updated Database")
    except:
        messagebox.showerror(
            "Connection Error", "Looks like you are not connected to internet."
        )


# ----Initilisation and making a canvas : Begin ---
root = tk.Tk()
root.resizable(0, 0)

canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
canvas.pack()

background_image = tk.PhotoImage(file="image.png")
background_label = tk.Label(root, image=background_image)
background_label.place(relwidth=1, relheight=1)

# ----Initilisation and making a canvas : End ---

# ---- top frame: Begin -----
top_frame = tk.Frame(root, bg="#80c1ff", bd=5)
top_frame.place(relx=0.5, rely=0.05, relwidth=0.9, relheight=0.1, anchor="n")

# ------Lower frame: Begin----
lower_frame = tk.Frame(root, bg="#80c1ff", bd=10)
lower_frame.place(relx=0.5, rely=0.15, relwidth=0.9, relheight=0.55, anchor="n")

# -----Bottom Frame -----

bottom_frame = tk.Frame(root, bg="#80c1ff", bd=5)
bottom_frame.place(relx=0.5, rely=0.71, relwidth=0.9, relheight=0.18, anchor="n")

# Text entry in top frame
entry = tk.Entry(top_frame, font=("courier", 12))
entry.place(relwidth=0.6, relheight=1)

# Get results button in top frame
button = tk.Button(
    top_frame,
    text="Get Results",
    font=("courier", 12),
    command=lambda: get_data(entry.get()),
)
button.place(relx=0.7, relwidth=0.3, relheight=1)

# -----Close Button----

close_button = tk.Button(root, text="Close", bg="gray", command=root.destroy)
close_button.place(relx=0.4, rely=0.9, relwidth=0.2, relheight=0.05)

# -----Update Button----

update_button = tk.Button(root, text="Update DB", bg="gray", command=update_command)
update_button.place(relx=0.75, rely=0.9, relwidth=0.2, relheight=0.05)

# ----Search Button-----
search_button = tk.Button(
    root, text="Search", bg="gray", command=lambda: search_command(entry.get())
)
search_button.place(relx=0.05, rely=0.9, relwidth=0.2, relheight=0.05)


label = tk.Label(lower_frame, font=("courier", 14))
label.place(relwidth=1, relheight=1)

label_bottom = tk.Label(bottom_frame, font=("courier", 12))
label_bottom.place(relwidth=1, relheight=1)

# ---- Key Bindings --------
root.bind("<Return>", lambda event=None: button.invoke())
root.bind("<Control-f>", lambda event=None: search_button.invoke())
root.bind("<Control-q>", lambda event=None: close_button.invoke())

root.mainloop()
