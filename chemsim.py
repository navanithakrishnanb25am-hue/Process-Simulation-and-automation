import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# ---------- Simulation Function ----------
def run_simulation():

    try:
        global t, C, P

        C0 = float(entry_c0.get())
        k = float(entry_k.get())
        t_max = float(entry_time.get())

        t = np.linspace(0, t_max, 100)

        C = C0 * np.exp(-k*t)
        P = C0 - C

        final_A = C[-1]
        final_B = P[-1]

        label_A.config(text=f"{final_A:.3f} mol/L")
        label_B.config(text=f"{final_B:.3f} mol/L")

        plt.figure()
        plt.plot(t, C, label="Reactant A")
        plt.plot(t, P, label="Product B")

        plt.xlabel("Time (min)")
        plt.ylabel("Concentration (mol/L)")
        plt.title("Concentration vs Time")
        plt.legend()
        plt.grid()

        plt.show()

    except:
        messagebox.showerror("Error","Please enter valid input values")


# ---------- Optimization ----------
def optimize_temperature():

    try:

        C0 = float(entry_c0.get())
        k = float(entry_k.get())

        temps = np.linspace(50,150,100)
        yields = []

        for T in temps:
            k_temp = k*(T/100)
            y = C0*(1-np.exp(-k_temp*10))
            yields.append(y)

        max_yield = max(yields)
        optimal_temp = temps[yields.index(max_yield)]

        label_temp.config(text=f"{optimal_temp:.2f} °C")
        label_yield.config(text=f"{max_yield:.2f} mol/L")

        plt.figure()
        plt.plot(temps,yields)

        plt.xlabel("Temperature (°C)")
        plt.ylabel("Yield")
        plt.title("Yield vs Temperature")
        plt.grid()

        plt.show()

    except:
        messagebox.showerror("Error","Run simulation first")


# ---------- Export CSV ----------
def export_csv():

    try:

        data = pd.DataFrame({
            "Time": t,
            "Reactant_A": C,
            "Product_B": P
        })

        file = filedialog.asksaveasfilename(defaultextension=".csv")

        data.to_csv(file,index=False)

        messagebox.showinfo("Success","Results exported successfully!")

    except:
        messagebox.showerror("Error","Run simulation first")


# ---------- Save Graph ----------
def save_graph():

    try:

        plt.figure()

        plt.plot(t,C,label="Reactant A")
        plt.plot(t,P,label="Product B")

        plt.xlabel("Time (min)")
        plt.ylabel("Concentration")
        plt.title("Reaction Graph")

        plt.legend()
        plt.grid()

        file = filedialog.asksaveasfilename(defaultextension=".png")

        plt.savefig(file)

        messagebox.showinfo("Saved","Graph saved successfully!")

    except:
        messagebox.showerror("Error","Run simulation first")


# ---------- Main Window ----------
root = tk.Tk()
root.title("ChemSim - Chemical Process Simulator")
root.geometry("750x500")

title = tk.Label(root,
text="ChemSim – Process Simulation and Optimization Software",
font=("Arial",16,"bold"))

title.pack(pady=10)

# ---------- Input Frame ----------
frame_input = ttk.LabelFrame(root,text="Input Parameters")
frame_input.pack(fill="x",padx=10,pady=10)

ttk.Label(frame_input,text="Initial Concentration (C0)").grid(row=0,column=0,padx=10,pady=5)
entry_c0 = ttk.Entry(frame_input)
entry_c0.insert(0,"1")
entry_c0.grid(row=0,column=1)

ttk.Label(frame_input,text="Reaction Rate Constant (k)").grid(row=1,column=0,padx=10,pady=5)
entry_k = ttk.Entry(frame_input)
entry_k.insert(0,"0.2")
entry_k.grid(row=1,column=1)

ttk.Label(frame_input,text="Reaction Time (min)").grid(row=2,column=0,padx=10,pady=5)
entry_time = ttk.Entry(frame_input)
entry_time.insert(0,"20")
entry_time.grid(row=2,column=1)

sim_btn = ttk.Button(frame_input,text="Run Simulation",command=run_simulation)
sim_btn.grid(row=3,column=0,columnspan=2,pady=10)


# ---------- Results Frame ----------
frame_results = ttk.LabelFrame(root,text="Simulation Results")
frame_results.pack(fill="x",padx=10,pady=10)

ttk.Label(frame_results,text="Final Concentration of A").grid(row=0,column=0,padx=10,pady=5)
label_A = ttk.Label(frame_results,text="---")
label_A.grid(row=0,column=1)

ttk.Label(frame_results,text="Final Concentration of B").grid(row=1,column=0,padx=10,pady=5)
label_B = ttk.Label(frame_results,text="---")
label_B.grid(row=1,column=1)


# ---------- Optimization Frame ----------
frame_opt = ttk.LabelFrame(root,text="Optimization")
frame_opt.pack(fill="x",padx=10,pady=10)

opt_btn = ttk.Button(frame_opt,text="Optimize Temperature",command=optimize_temperature)
opt_btn.grid(row=0,column=0,columnspan=2,pady=10)

ttk.Label(frame_opt,text="Optimal Temperature").grid(row=1,column=0,padx=10,pady=5)
label_temp = ttk.Label(frame_opt,text="---")
label_temp.grid(row=1,column=1)

ttk.Label(frame_opt,text="Maximum Yield").grid(row=2,column=0,padx=10,pady=5)
label_yield = ttk.Label(frame_opt,text="---")
label_yield.grid(row=2,column=1)


# ---------- Extra Features ----------
frame_extra = ttk.LabelFrame(root,text="Export / Save")
frame_extra.pack(fill="x",padx=10,pady=10)

csv_btn = ttk.Button(frame_extra,text="Export Results to CSV",command=export_csv)
csv_btn.grid(row=0,column=0,padx=10,pady=10)

save_btn = ttk.Button(frame_extra,text="Save Graph as PNG",command=save_graph)
save_btn.grid(row=0,column=1,padx=10,pady=10)


root.mainloop()