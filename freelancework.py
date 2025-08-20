DATA_FILE = "data_store.py"

# Initialize data
clients = {}
projects = {}

def load_data():
    global clients, projects
    try:
        local_vars = {}
        with open(DATA_FILE, "r") as f:
            exec(f.read(), {}, local_vars)
        clients = local_vars.get("clients", {})
        projects = local_vars.get("projects", {})
    except:
        clients = {}
        projects = {}

def save_data():
    with open(DATA_FILE, "w") as f:
        f.write("clients = " + repr(clients) + "\n")
        f.write("projects = " + repr(projects) + "\n")

def add_client():
    client_id = str(len(clients) + 1)
    name = input("Enter client name: ").strip()
    email = input("Enter client email: ").strip()
    phone = input("Enter client phone: ").strip()
    clients[client_id] = {"name": name, "email": email, "phone": phone}
    save_data()
    print(f"Client '{name}' added with ID {client_id}.")

def list_clients():
    if not clients:
        print("No clients found.")
    else:
        print("Clients:")
        for cid, c in clients.items():
            print(f"  {cid}: {c['name']} (Email: {c['email']}, Phone: {c['phone']})")

def add_project():
    if not clients:
        print("No clients yet. Please add a client first.")
        return
    list_clients()
    client_id = input("Enter client ID for the project: ")
    if client_id not in clients:
        print("Invalid client ID.")
        return
    project_id = str(len(projects) + 1)
    title = input("Enter project title: ")
    description = input("Enter project description: ")
    try:
        hourly_rate = float(input("Enter hourly rate: "))
        if hourly_rate < 0:
            print("Hourly rate cannot be negative.")
            return
    except:
        print("Invalid hourly rate. Setting to 0.")
        hourly_rate = 0.0
    projects[project_id] = {
        "client_id": client_id,
        "title": title,
        "description": description,
        "hourly_rate": hourly_rate,
        "hours_worked": 0.0
    }
    save_data()
    print(f"Project '{title}' added with ID {project_id}.")

def log_hours():
    if not projects:
        print("No projects found.")
        return
    print("Projects:")
    for pid, p in projects.items():
        print(f"  {pid}: {p['title']} (Hours worked: {p['hours_worked']})")
    project_id = input("Enter project ID to log hours: ")
    if project_id not in projects:
        print("Invalid project ID.")
        return
    try:
        hours = float(input("Enter hours worked: "))
        if hours < 0:
            print("Hours cannot be negative.")
            return
    except:
        print("Invalid input for hours.")
        return
    projects[project_id]["hours_worked"] += hours
    save_data()
    print(f"Logged {hours} hours for project '{projects[project_id]['title']}'.")

def generate_invoice():
    if not projects:
        print("No projects found.")
        return
    print("Projects:")
    for pid, p in projects.items():
        print(f"  {pid}: {p['title']}")
    project_id = input("Enter project ID to generate invoice: ")
    if project_id not in projects:
        print("Invalid project ID.")
        return
    project = projects[project_id]
    client = clients[project["client_id"]]
    total = project["hours_worked"] * project["hourly_rate"]
    print("\n--- INVOICE ---")
    print(f"Client: {client['name']} ({client['email']})")
    print(f"Project: {project['title']}")
    print(f"Description: {project['description']}")
    print(f"Hours Worked: {project['hours_worked']}")
    print(f"Hourly Rate: ₹{project['hourly_rate']}")
    print(f"Total Amount: ₹{total}")
    print("----------------\n")

def main_menu():
    load_data()
    while True:
        print("\nFreelance Work Management System")
        print("1. Add Client")
        print("2. List Clients")
        print("3. Add Project")
        print("4. Log Hours")
        print("5. Generate Invoice")
        print("6. Exit")
        choice = input("Choose an option: ")
        if choice == "1":
            add_client()
        elif choice == "2":
            list_clients()
        elif choice == "3":
            add_project()
        elif choice == "4":
            log_hours()
        elif choice == "5":
            generate_invoice()
        elif choice == "6":
            print("Exiting. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()
