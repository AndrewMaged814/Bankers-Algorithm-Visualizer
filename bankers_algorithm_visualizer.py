import customtkinter

# Modes: "System" (standard), "Dark", "Light"
customtkinter.set_appearance_mode("System")
# Themes: "blue" (standard), "green", "dark-blue"
customtkinter.set_default_color_theme("green")


class BankersAlgorithm:
    def __init__(self, available, currently_allocated, max_need):
        self.available = available
        self.currently_allocated = currently_allocated
        self.max_need = max_need

    def is_safe_state(self):
        global delay
        resources = len(self.available)
        running = [True] * len(self.currently_allocated)
        count = len(self.currently_allocated)
        for i in range(len(self.currently_allocated)):
            if running[i]:
                executing = True

                for j in range(resources):
                    if self.max_need[i][j] - self.currently_allocated[i][j] > self.available[j]:
                        executing = False
                        break
                if executing:
                    app.after(delay, execute_with_delay, i+1)
                    running[i] = False
                    count -= 1
                    for j in range(resources):
                        self.available[j] += self.currently_allocated[i][j]
                    delay += 5000
        if count == 0:
            app.after(delay, execute_with_delay_safe,
                      "The processes are in a safe state.", count)
            return True
        else:
            app.after(delay, execute_with_delay_safe,
                      "The processes are in an unsafe state.", count)
            return False

    def request_resources(self, process_num, request):
        global delay
        resources = len(self.available)
        # Check if the request can be granted
        for i in range(resources):
            if request[i] > self.available[i]:
                app.after(delay, execute_with_delay_safe,
                          "Error: Requested resources exceed available resources.", 1)
                return False
            if request[i] > self.max_need[process_num][i] - self.currently_allocated[process_num][i]:
                app.after(delay, execute_with_delay_safe,
                          "Error: Requested resources exceed maximum need of the process.", 1)
                return False

        # Try to allocate the requested resources and check if the new state is safe
        for i in range(resources):
            self.available[i] -= request[i]
            self.currently_allocated[process_num][i] += request[i]

        if self.is_safe_state():
            return True
        else:
            # The new state is not safe, so undo the allocation
            for i in range(resources):
                self.available[i] += request[i]
                self.currently_allocated[process_num][i] -= request[i]
            return False


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.bankers_algorithm = None
        # configure window
        self.title("Banker's Algorithm visualizer")
        self.geometry(f"{1000}x{580}")
        self.grid_rowconfigure((0, 1, 2, 3), weight=1)
        self.grid_columnconfigure((0, 1, 2, 3), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(
            self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(
            self.sidebar_frame, text="Banker's\nAlgorithm", font=customtkinter.CTkFont(size=40, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=(20, 10), pady=(20, 10))

        self.choice_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Show status", "Request resources"],
                                                              command=self.choose_status_request)
        self.choice_optionemenu.grid(
            row=5, column=0, padx=20, pady=(10, 10))
        self.appearance_mode_label = customtkinter.CTkLabel(
            self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=8, column=0, padx=10, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(
            row=9, column=0, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(
            self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=10, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=11, column=0, padx=20, pady=(10, 20))

        self.simualte_frame = customtkinter.CTkFrame(
            self, fg_color="transparent")
        self.simualte_frame.grid(
            row=3, column=1, padx=(10, 0), pady=(10, 0), sticky="nsew", columnspan=3)

        self.progressbar_1 = customtkinter.CTkProgressBar(
            master=self.simualte_frame, width=500)
        self.progressbar_1.grid(row=3, column=1, columnspan=3, padx=(
            20, 0), pady=(30, 30), sticky="nsew")
        self.sim_label = customtkinter.CTkLabel(
            master=self.simualte_frame, text="Waiting to start simulation", font=customtkinter.CTkFont(size=15, weight="normal"))
        self.sim_label.grid(row=2, column=1, columnspan=3, padx=(
            20, 0), pady=(30, 30), sticky="nsew")
        self.start_simulation_btn = customtkinter.CTkButton(
            master=self.simualte_frame, command=self.start_simulation_animation, text="Simulate", fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"))
        self.start_simulation_btn.grid(row=3, column=4, padx=(
            20, 20), pady=(20, 20), sticky="e")

        self.input_frame = customtkinter.CTkFrame(
            self, fg_color="transparent")
        self.input_frame.grid(
            row=0, column=1, padx=(10, 0), pady=(10, 0), columnspan=3, rowspan=3)

        self.label_ava_matrix = customtkinter.CTkLabel(
            self.input_frame, text="Available matrix", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.label_ava_matrix.grid(row=0, column=1,  padx=10, pady=(10, 5))
        self.ava_entry = customtkinter.CTkEntry(
            self.input_frame, placeholder_text="3 1 1 2")
        self.ava_entry.grid(row=1, column=1,  padx=20,
                            pady=(20, 10), sticky="nsew")

        self.label_max_res = customtkinter.CTkLabel(
            self.input_frame, text="Total resources", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.label_max_res.grid(row=0, column=2, padx=10, pady=(10, 5))
        self.max_res_entry = customtkinter.CTkEntry(
            self.input_frame, placeholder_text="6 5 7 6")
        self.max_res_entry.grid(row=1, column=2,  padx=20,
                                pady=(20, 10), sticky="nsew")

        self.label_allocated = customtkinter.CTkLabel(
            self.input_frame, text="Current Allocated", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.label_allocated.grid(row=2, column=1, padx=20, pady=(20, 10))

        self.text_box_allocated = customtkinter.CTkTextbox(self.input_frame)
        self.text_box_allocated.grid(row=3, column=1, padx=(
            20, 0), pady=(20, 10), sticky="nsew")

        self.label_max = customtkinter.CTkLabel(
            self.input_frame, text="Maximum need", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.label_max.grid(row=2, column=2, padx=20, pady=(20, 10))

        self.text_box_max = customtkinter.CTkTextbox(self.input_frame)
        self.text_box_max.grid(row=3, column=2, padx=20,
                               pady=(20, 10), sticky="nsew")

        self.label_n_process = customtkinter.CTkLabel(
            self.input_frame, text="Number of processes", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.label_n_process.grid(row=0, column=3, padx=10, pady=(20, 10))
        self.n_processes_entry = customtkinter.CTkEntry(
            self.input_frame, placeholder_text="3")
        self.n_processes_entry.grid(row=1, column=3, padx=10, pady=(20, 10))
        self.label_n_res = customtkinter.CTkLabel(
            self.input_frame, text="Number of Resources", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.label_n_res.grid(row=2, column=3, padx=10, pady=(20, 10))
        self.n_resources_entry = customtkinter.CTkEntry(
            self.input_frame, placeholder_text="4")
        self.n_resources_entry.grid(row=3, column=3, padx=20,
                                    pady=(20, 10), sticky='n')

        self.appearance_mode_optionemenu.set("Dark")
        self.scaling_optionemenu.set("100%")
        self.progressbar_1.configure(mode="indeterminnate")

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def choose_status_request(self, choise: str):
        if choise == "Request resources":
            self.request_res_entry = customtkinter.CTkEntry(
                self.sidebar_frame, placeholder_text="Request resource")
            self.request_res_entry.grid(
                row=6, column=0, pady=10, padx=20, sticky='n')
            self.request_process_entry = customtkinter.CTkEntry(
                self.sidebar_frame, placeholder_text="Request process")
            self.request_process_entry.grid(
                row=7, column=0, pady=10, padx=20, sticky='n')
        else:
            if hasattr(self, 'request_process_entry'):
                self.request_process_entry.grid_remove()
            if hasattr(self, 'request_res_entry'):
                self.request_res_entry.grid_remove()
        return choise

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def start_simulation_animation(self):
        try:
            global delay
            delay = 0
            available, curr_aloc, max_need = app.get_input()

            # Parse input and create an instance of BankersAlgorithm
            available = [int(x) for x in available.split()]
            curr_aloc = [[int(i) for i in line.split()]
                         for line in curr_aloc.split('\n')]
            max_need = [[int(i) for i in line.split()]
                        for line in max_need.split('\n')]

            self.bankers_algorithm = BankersAlgorithm(
                available, curr_aloc, max_need)

            if not any(curr_aloc) or not any(max_need) or available == []:
                self.sim_label.configure(text="Insufficient inputs ")
                return
            
            self.progressbar_1.start()
            self.sim_label.configure(text_color="white")
            if self.choice_optionemenu.get() == "Show status":
                self.bankers_algorithm.is_safe_state()
            else:
                req_process, req_res = app.get_input_req()
                req_process = int(req_process)
                req_res = [int(x) for x in req_res.split()]

                if self.bankers_algorithm.request_resources(req_process - 1, req_res):
                    app.after(delay, execute_with_delay_safe,
                              "Request granted.", 0)
                else:
                    app.after(5000, execute_with_delay_safe,
                              "Request denied.", 1)
        except Exception as e:
            self.sim_label.configure(text="Invalid input")
            print("Error: " + str(e))

    def get_input_req(self):
        return self.request_process_entry.get(), self.request_res_entry.get()

    def get_input(self):
        return self.ava_entry.get(), self.text_box_allocated.get("1.0", 'end-1c'), self.text_box_max.get("1.0", 'end-1c')


def execute_with_delay_safe(message, flag):
    if flag == 0:
        app.sim_label.configure(text_color="green")
    else:
        app.sim_label.configure(text_color="red")
    app.sim_label.configure(text=message)
    app.progressbar_1.stop()


def execute_with_delay(process_number):
    app.sim_label.configure(text=f"Process {process_number} is executing")


if __name__ == "__main__":
    app = App()
    app.mainloop()
