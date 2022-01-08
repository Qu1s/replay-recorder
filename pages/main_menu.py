from tkinter import Button, END, Entry, filedialog, Frame, Label, OptionMenu, _setit
from subprocess import Popen
from os import listdir


class MainMenu(Frame):
	def __init__(self, parent, controller):

		Frame.__init__(self, parent)
		self.controller = controller

		def choose_replay():
			file = filedialog.askopenfile()
			if file:
				replay.config(state='normal')
				self.controller.replay_path = file.name
				replay.delete(0, END)
				replay.insert(END, file.name)
				replay.config(state='disabled')
		
		def update_skin_selector(event):
			if self.controller.is_dirs_valid():
				skin_selector['menu'].delete(0, 'end')
				for item in listdir(self.controller.config['General']['OsuSkinsDir']):
					skin_selector['menu'].add_command(label=item, command=_setit(self.controller.skin_name, item))

		def render_video():
			if not self.controller.replay_path:
				print('Не выбран файл реплея')
				return
			Popen(f'danser -quickstart \
									  -skin="{self.controller.skin_name.get()}" \
									  -replay="{self.controller.replay_path}" \
									  -record')
		# Интерфейс для выбора реплея
		Label(self, text='Selected replay', width=20).grid(row=0, column=0)
		replay = Entry(self, width=50, state='disabled')
		replay.insert(END, self.controller.replay_path)
		replay.grid(row=0, column=1)
		Button(self, text='Choose replay', command=lambda: choose_replay(), width=20).grid(row=0, column=2)

		# Интерфейс для выбора скина
		Label(self, text='Selected skin', width=20).grid(row=1, column=0)
		skin_list = ['default']
		self.controller.skin_name.set(skin_list[0])
		if self.controller.is_dirs_valid():
			for item in listdir(self.controller.config['General']['OsuSkinsDir']):
				skin_list.append(item)
		skin_selector = OptionMenu(self, self.controller.skin_name, *skin_list)
		skin_selector.bind('<1>', update_skin_selector)
		skin_selector.grid(row=1, column=1)

		Button(self, text='Render video', command=lambda: render_video(), width=20).grid(row=2, column=0)
		Button(self, text='Settings', command=lambda: controller.show_frame('Settings'), width=20).grid(row=3, column=2)
