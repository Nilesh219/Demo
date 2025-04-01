import socket
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap import Style
from tkinter import scrolledtext

class ControllerApp:
    def __init__(self, master):
        self.master = master
        style = Style(theme='darkly')
        self.master.title("Controller")
        self.master.geometry("700x700")
        icon = tk.PhotoImage(file="C_image.png")
        self.master.iconphoto(False, icon)

        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)  # Handle window close
        
      
        
        self.frame = tk.Frame(self.master)  # Corrected root to master
        self.frame.pack(pady=20)


        # Controller IP Section
        controller_frame = tk.Frame(self.frame)
        controller_frame.grid(row=0, column=0, columnspan=5, pady=10)

        tk.Label(controller_frame, text="Controller IP:").grid(row=0, column=0, padx=5, pady=5)
        self.controller_ip_entry = tk.Entry(controller_frame, width=16)
        self.controller_ip_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(controller_frame, text="Port:").grid(row=0, column=2, padx=5, pady=5)
        self.controller_port_entry = tk.Entry(controller_frame, width=5)  # Port Input
        self.controller_port_entry.grid(row=0, column=3, padx=5, pady=5)

        self.controller_connect_button = tk.Button(controller_frame, text="Connect", command=self.connect)
        self.controller_connect_button.grid(row=0, column=4, padx=5, pady=5)

        # Set Speed & Set Position - Centered
        set_frame = tk.Frame(self.frame)
        set_frame.grid(row=1, column=0, columnspan=4, pady=10)

        tk.Label(set_frame, text="Set Speed:").grid(row=0, column=0, padx=5, pady=5)
        self.speed_entry = tk.Entry(set_frame, width=10)
        self.speed_entry.grid(row=0, column=1, padx=5, pady=5)
        self.set_speed_button = tk.Button(set_frame, text="Set Speed", command=self.set_speed)
        self.set_speed_button.grid(row=0, column=2, padx=5, pady=5)

        tk.Label(set_frame, text="Set Position:").grid(row=1, column=0, padx=5, pady=5)
        self.position_entry = tk.Entry(set_frame, width=10)
        self.position_entry.grid(row=1, column=1, padx=5, pady=5)
        self.set_position_button = tk.Button(set_frame, text="Set Position", command=self.set_position)
        self.set_position_button.grid(row=1, column=2, padx=5, pady=5)
        

        # Button Grid - Centered
        button_frame = tk.Frame(self.frame)
        button_frame.grid(row=2, column=0, columnspan=4, pady=10)

        self.enable_encoder_button = tk.Button(button_frame, text="Enable Encoder", width=15, command=self.enable_encoder)
        self.enable_encoder_button.grid(row=0, column=0, padx=5, pady=2)

        self.disable_encoder_button = tk.Button(button_frame, text="Disable Encoder", width=15, command=self.disable_encoder)
        self.disable_encoder_button.grid(row=0, column=1, padx=5, pady=2)

        self.move_motor_Home_button = tk.Button(button_frame, text="Home Position", width=15, command=self.move_motor_home)
        self.move_motor_Home_button.grid(row=1, column=0, padx=5, pady=2)

        self.move_extreme_button = tk.Button(button_frame, text="Extreme Position", width=15, command=self.move_extreme)
        self.move_extreme_button.grid(row=1, column=1, padx=5, pady=2)

        self.move_forward_button = tk.Button(button_frame, text="Move Forward", width=15, command=self.move_forward)
        self.move_forward_button.grid(row=2, column=0, padx=5, pady=2)

        self.move_reverse_button = tk.Button(button_frame, text="Move Reverse", width=15, command=self.move_reverse)
        self.move_reverse_button.grid(row=2, column=1, padx=5, pady=2)

        self.move_motor_button = tk.Button(button_frame, text="Move Motor", width=15, command=self.move_motor)
        self.move_motor_button.grid(row=3, column=0, padx=5, pady=2)

        self.emergency_stop_button = tk.Button(button_frame, text="Emergency Stop", width=15, command=self.emergency_stop)
        self.emergency_stop_button.grid(row=3, column=1, padx=5, pady=2)

        self.help_button = tk.Button(button_frame, text="Help", width=15, command=self.help)
        self.help_button.grid(row=4, column=0, padx=5, pady=2)

        self.read_speed_position_button = tk.Button(button_frame, text="Read Speed & Position", width=15, command=self.read_speed_position)
        self.read_speed_position_button.grid(row=4, column=1, padx=5, pady=2)

        self.read_current_position_button = tk.Button(button_frame, text="Read Current Position", width=15, command=self.read_current_position)
        self.read_current_position_button.grid(row=5, column=0, padx=5, pady=2)

        self.read_set_speed_button = tk.Button(button_frame, text="Read Set Speed", width=15, command=self.read_set_speed)
        self.read_set_speed_button.grid(row=5, column=1, padx=5, pady=2)

        # Reset IP Section
        reset_frame = tk.Frame(self.frame)
        reset_frame.grid(row=11, column=0, columnspan=4, pady=10)

        tk.Label(reset_frame, text="Reset IP:").grid(row=0, column=0, padx=5, pady=5)
        self.reset_ip_entry = tk.Entry(reset_frame, width=16)
        self.reset_ip_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(reset_frame, text="Port:").grid(row=0, column=2, padx=5, pady=5)
        self.reset_port_entry = tk.Entry(reset_frame, width=5)  # Port Input
        self.reset_port_entry.grid(row=0, column=3, padx=5, pady=5)

        self.reset_button = tk.Button(reset_frame, text="Reset", command=self.reset_ip)
        self.reset_button.grid(row=0, column=4, padx=5, pady=5)

        # Output Text
        self.output_text = tk.Text(reset_frame, height=8, width=50)
        self.output_text.grid(row=1, column=0, columnspan=5, padx=5, pady=10)

        self.sock = None

    def connect(self):
        ip = self.controller_ip_entry.get()
        port = self.controller_port_entry.get()

        if not ip or not port:
            self.output_text.insert(tk.END, "Error: Please enter both IP and Port\n")
            return

        try:
            port = int(port)
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((ip, port))
            self.output_text.insert(tk.END, f"Connected to {ip}:{port}\n")
        except Exception as e:
            self.output_text.insert(tk.END, f"Error: {str(e)}\n")

    def send_command(self, command):
        if self.sock:
            try:
                self.sock.send(command.encode())  # Sending command
                response = self.sock.recv(1024)  # Receiving raw bytes

                try:
                    decoded_response = response.decode("utf-8")  # Try UTF-8
                except UnicodeDecodeError:
                    decoded_response = response.decode("ISO-8859-1", errors="ignore")  # Fallback

                formatted_text = f"\n[📤 SENT]   {command}\n[📥 RESPONSE]   {decoded_response}\n" 
                self.output_text.insert(tk.END, formatted_text)
                self.output_text.insert(tk.END, "-" * 50 + "\n")  # Separator for clarity
                self.output_text.yview(tk.END)  # Auto-scroll to the latest response
                
            except Exception as e:
                self.output_text.insert(tk.END, f"\n[❌ ERROR]   {str(e)}\n")
                self.output_text.insert(tk.END, "-" * 50 + "\n")  # Separator
        else:
            self.output_text.insert(tk.END, "\n[⚠️ ERROR]   Not connected to controller\n")
            self.output_text.insert(tk.END, "-" * 50 + "\n")  # Separator


    def reset_ip(self):
        ip_address = self.reset_ip_entry.get()
        port = self.reset_port_entry.get()

        if not ip_address or not port:
            self.output_text.insert(tk.END, "Error: Please enter both IP and Port\n")
            return

        try:
            ip_parts = ip_address.split('.')
            if len(ip_parts) != 4 or not all(part.isdigit() and 0 <= int(part) <= 255 for part in ip_parts):
                self.output_text.insert(tk.END, "Error: Invalid IP format\n")
                return

            if not port.isdigit() or not (0 <= int(port) <= 65535):
                self.output_text.insert(tk.END, "Error: Invalid Port number\n")
                return

            commands = [
                f"A{ip_parts[0]}",
                f"B{ip_parts[1]}",
                f"C{ip_parts[2]}",
                f"D{ip_parts[3]}",
                f"E{port}",
                "rst"
            ]

            for cmd in commands:
                self.send_command(cmd)

        except Exception as e:
            self.output_text.insert(tk.END, f"Error: {str(e)}\n")

    def disconnect(self):
        if self.sock:
            try:
                self.sock.close()
                self.output_text.insert(tk.END, "Disconnected from controller\n")
            except Exception as e:
                self.output_text.insert(tk.END, f"Error disconnecting: {str(e)}\n")
        self.sock = None

    def on_closing(self):
        self.disconnect()
        self.master.destroy()
       

    def enable_encoder(self):
        self.send_command("encode")
    
    def disable_encoder(self):
        self.send_command("encoff")
    
    def move_motor_home(self):
        self.send_command("home")

    def move_motor(self):
        self.send_command("mx")

    def move_extreme(self):
        self.send_command("extr")
    
    def move_forward(self):
        self.send_command("fwd")
    
    def move_reverse(self):
        self.send_command("rev")
    
    def emergency_stop(self):
        self.send_command("stop")

    def read_speed_position(self):
        self.send_command("read")

    def help(self):
        self.send_command("help")
        help_text = """
        Available Commands:
        1. encode - Enable encoder
        2. encoff - Disable encoder
        3. home - Move motor to home position
        4. mx - Move motor
        5. extr - Move to extreme position
        6. fwd - Move forward
        7. rev - Move reverse
        8. stop - Emergency stop
        9. S<speed> - Set speed (e.g., S100)
        10. P<position> - Set position (e.g., P100)
        11. help - Show this help
        12. read - Read current speed and position
        13. rdPos - Read current position
        14. rdSpeed - Read set speed
        15. rst - Reset IP to default
        """
        self.output_text.insert(tk.END, help_text)

    def read_current_position(self):    
        self.send_command("rdPos")

    def read_set_speed(self):
        self.send_command("rdSpeed")
    
    def set_speed(self):
        speed = self.speed_entry.get()
        self.send_command(f"S{speed}") # e.g. S100 = 1 mm/s
    
    def set_position(self):
        position = self.position_entry.get()
        self.send_command(f"P{position}") # e.g. P100 = 1 mm

    def reset(self):
        self.send_command("rst")


if __name__ == "__main__":
    root = tk.Tk()
    app = ControllerApp(root)
    root.mainloop()
