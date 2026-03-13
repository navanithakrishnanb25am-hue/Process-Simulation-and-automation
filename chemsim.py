import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# ---------- Global Variables ----------
t = None
C = None
P = None
reactor_conc = []
reactor_index = []

# ---------- Simulation ----------
def run_simulation():

    try:
        global t, C, P, reactor_conc, reactor_index

        C0 = float(entry_c0.get())
        k = float(entry_k.get())
        t_max = float(entry_time.get())
        reactors = int(entry_reactors.get())

        t = np.linspace(0, t_max, 100)

        C = C0 * np.exp(-k * t)
        P = C0 - C

        final_A = C[-1]
        final_B = P[-1]

        label_A.config(text=f"{final_A:.3f} mol/L")
        label_B.config(text=f"{final_B:.3f} mol/L")

        # Reactor calculations
        reactor_conc = [C0]
        conc = C0

        for r in range(reactors):

            conc = conc * np.exp(-k * t_max / reactors)
            reactor_conc.append(conc)

        reactor_index = list(range(reactors+1))

        animate_reactors()

        plot_live_graph()

    except:
        messagebox.showerror("Error","Please enter valid input values")

# ---------- Live Graph ----------
def plot_live_graph():

    plt.figure()

    plt.ion()

    for i in range(len(t)):

        plt.clf()

        plt.plot(t[:i],C[:i],label="Reactant A")
        plt.plot(t[:i],P[:i],label="Product B")

        plt.xlabel("Time (min)")
        plt.ylabel("Concentration")

        plt.title("Real Time Reaction Simulation")

        plt.legend()
        plt.grid()

        plt.pause(0.02)

    plt.ioff()
    plt.show()

# ---------- Reactor Animation ----------
def animate_reactors():

    canvas.delete("all")

    reactors = int(entry_reactors.get())

    x_start = 50
    spacing = 120

    canvas.create_rectangle(x_start,120,x_start+80,180,fill="lightgreen")
    canvas.create_text(x_start+40,150,text="Feed")

    prev_x = x_start + 80

    for i in range(reactors):

        x = x_start + (i+1)*spacing

        canvas.create_line(prev_x,150,x,150,arrow=tk.LAST)

        # Color depends on concentration
        conc = reactor_conc[i]

        if conc > 0.7:
            color = "red"
        elif conc > 0.3:
            color = "yellow"
        else:
            color = "lightblue"

        canvas.create_rectangle(x,120,x+80,180,fill=color)

        canvas.create_text(x+40,150,text=f"R{i+1}")

        prev_x = x + 80

    x = x_start + (reactors+1)*spacing

    canvas.create_line(prev_x,150,x,150,arrow=tk.LAST)

    canvas.create_rectangle(x,120,x+80,180,fill="orange")

    canvas.create_text(x+40,150,text="Product")

# ---------- 3D Reactor Visualization ----------
def show_3d_plot():

    try:

        from mpl_toolkits.mplot3d import Axes3D

        reactors = len(reactor_conc)-1

        x = np.arange(reactors+1)
        y = reactor_conc
        z = np.zeros_like(x)

        fig = plt.figure()
        ax = fig.add_subplot(111,projection="3d")

        ax.bar3d(x,z,z,0.5,0.5,y)

        ax.set_xlabel("Reactor Number")
        ax.set_ylabel("")
        ax.set_zlabel("Concentration")

        plt.title("3D Reactor Concentration Profile")

        plt.show()

    except:
        messagebox.showerror("Error","Run simulation first")

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

# ---------- GUI ----------
root = tk.Tk()

root.title("ChemSim Pro – Advanced Chemical Simulator")

root.geometry("900x700")

title = tk.Label(root,
text="ChemSim Pro – Chemical Process Simulation Software",
font=("Arial",16,"bold"))

title.pack(pady=10)

# ---------- Input ----------
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

ttk.Label(frame_input,text="Number of Reactors").grid(row=3,column=0,padx=10,pady=5)
entry_reactors = ttk.Entry(frame_input)
entry_reactors.insert(0,"3")
entry_reactors.grid(row=3,column=1)

ttk.Button(frame_input,text="Run Simulation",command=run_simulation).grid(row=4,column=0,columnspan=2,pady=10)

# ---------- Results ----------
frame_results = ttk.LabelFrame(root,text="Simulation Results")
frame_results.pack(fill="x",padx=10,pady=10)

ttk.Label(frame_results,text="Final Concentration of Reactant A").grid(row=0,column=0,padx=10,pady=5)
label_A = ttk.Label(frame_results,text="---")
label_A.grid(row=0,column=1)

ttk.Label(frame_results,text="Final Concentration of Product B").grid(row=1,column=0,padx=10,pady=5)
label_B = ttk.Label(frame_results,text="---")
label_B.grid(row=1,column=1)

# ---------- Optimization ----------
frame_opt = ttk.LabelFrame(root,text="Optimization")
frame_opt.pack(fill="x",padx=10,pady=10)

ttk.Button(frame_opt,text="Optimize Temperature",command=optimize_temperature).grid(row=0,column=0,columnspan=2,pady=10)

ttk.Label(frame_opt,text="Optimal Temperature").grid(row=1,column=0)
label_temp = ttk.Label(frame_opt,text="---")
label_temp.grid(row=1,column=1)

ttk.Label(frame_opt,text="Maximum Yield").grid(row=2,column=0)
label_yield = ttk.Label(frame_opt,text="---")
label_yield.grid(row=2,column=1)

# ---------- Diagram ----------
frame_diagram = ttk.LabelFrame(root,text="Process Flow Diagram")
frame_diagram.pack(fill="both",expand=True,padx=10,pady=10)

canvas = tk.Canvas(frame_diagram,width=750,height=250,bg="white")
canvas.pack()

# ---------- 3D Button ----------
ttk.Button(root,text="Show 3D Reactor Visualization",command=show_3d_plot).pack(pady=10)

# ---------- Export ----------
frame_extra = ttk.LabelFrame(root,text="Export / Save")
frame_extra.pack(fill="x",padx=10,pady=10)

ttk.Button(frame_extra,text="Export Results to CSV",command=export_csv).grid(row=0,column=0,padx=10,pady=10)
ttk.Button(frame_extra,text="Save Graph as PNG",command=save_graph).grid(row=0,column=1,padx=10,pady=10)

root.mainloop()