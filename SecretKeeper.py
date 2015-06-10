#!/usr/bin/env python

import Tkinter as tk
import ttk
from ScrolledText import ScrolledText
from sys import argv
from hashlib import sha512
from itertools import cycle

#default key (password) = 'nicol'
data = 'ZxpLVPJD43PjTJsBma4YpmdqLFF8LcMJv4q2fXH/SeaRFg==' #default 

data_delim = ' '.join(('####dammed','data####\n'))
magic_string = 'Nicol'
geometry = "400x500+300+300" #default 

def convert(data, key):
	'''simple XOR encryption based on the password hash'''
	key = sha512(key).digest()
	return ''.join(chr(ord(d)^ord(k)) for d,k in zip(data, cycle(key)))

def encrypt(data, key):
	'''add magic string, encrypt, and convert to base64'''
	return convert(magic_string + data, key).encode('base64')

def decrypt(data, key):
	'''decode from base64, decrypt, check magic string (password worked),
	and return without magic string, or returns None if password did not work'''
	data = convert(data.decode('base64'), key)
	if data.startswith(magic_string):
		return data[len(magic_string):]

def save(new_data, key, new_geo=None):
	'''encrypt and save new data to this file
	new_data is an unencrypted string
	optionally provide a new geometry string'''
	global data #technically not needed in GUI mode since this is called only when quitting
	fn = __file__
	if fn.endswith('.pyc'):
		fn = fn[:-1] #an import would compile the file
	with open(fn, "r+") as f:
		contents = f.read().split(data_delim)
		if len(contents) != 3:
			raise TypeError, "File is not of the right type"
		data = encrypt(new_data, key)
		contents[1] = "geometry='%s'\n" % (new_geo or geometry)
		contents[1] += "data='''\n%s'''\n" % data
		#erase file and write new contents
		f.seek(0)
		f.truncate()
		f.write(data_delim.join(contents))
		
def rekey(old_key, new_key):
	'''change key for the global data'''
	secret = decrypt(data,old_key)
	if secret is None:
		raise ValueError, "old_key is wrong"
	save(secret, new_key)

class Window(ttk.Frame):
	def __init__(self, parent):
		self.tab_delim = "\n=====++++++=====\n"
		self.tabs = []
		self.dirty = False
		
		ttk.Frame.__init__(self, parent)
		self.parent = parent
		self.parent.title("Very Secret Things")
		self.style = ttk.Style()
		self.style.theme_use("default")
		self.pack(fill=tk.BOTH, expand=1)
		self.nb = ttk.Notebook(self)
		self.nb.pack(fill=tk.BOTH, expand=1)

		self.saveButton = ttk.Button(self, text="Close", command=self.save)
		self.saveButton.pack(side=tk.RIGHT, padx=5, pady=5)
		# I don't feel like making a rekey dialog atm
		#~ rekeyButton = ttk.Button(self, text="Re-Key", command=self.rekey)
		#~ rekeyButton.pack(side=tk.RIGHT, padx=5, pady=5)
		addButton = ttk.Button(self, text="Add Tab", command=self.add_tab)
		addButton.pack(side=tk.LEFT, padx=5, pady=5)
		delButton = ttk.Button(self, text="Delete Tab", command=self.rem_tab)
		delButton.pack(side=tk.LEFT, padx=5, pady=5)
		
		#add search tab
		f = ttk.Frame(self.nb)
		self.search = ttk.Entry(f)
		self.search.focus()
		self.search.pack(fill=tk.BOTH)
		self.search.bind("<KeyRelease>", self.search_key_press)
		self.search_result = ScrolledText(f, relief=tk.RAISED, wrap=tk.WORD, state=tk.DISABLED)
		self.search_result.pack(fill=tk.BOTH, expand=1)
		self.nb.add(f, text='search')
		
		#add other tabs
		for text in self.parent.secret.split(self.tab_delim):
			self.add_tab(text, dirty=False)
		self.nb.select(self.nb.tabs()[0]) #select search tab
	
	def search_key_press(self, key):
		'''if search key is found displays that line and all lines below
		it until an empty line is reached.'''
		search = self.search.get()
		found = []
		state = None
		for line in self.parent.secret.splitlines():
			if state is None:
				if search in line.lower():
					state = line
			else:
				if line.strip() == "":
					found.append(state)
					state = None
				else:
					state += "\n"+line
		if state is not None:
			found.append(state)
		self.search_result.config(state=tk.NORMAL)
		self.search_result.delete("0.0", tk.END)
		self.search_result.insert(tk.INSERT, "\n\n".join(found))
		self.search_result.config(state=tk.DISABLED)
	
	def save(self):
		if self.dirty: #file changed
			save(self.parent.secret, self.parent.key, self.parent.geometry())
		self.quit()
	
	def rem_tab(self):
		tabid = self.nb.select()
		if self.nb.index(tabid) > 0:
			#index minus 1 to account for search tab
			del self.tabs[self.nb.index(tabid)-1] 
			self.nb.forget(tabid)
			self.update()
	
	def add_tab(self, text='new', dirty=True):
		f = ttk.Frame(self.nb)
		# see http://stackoverflow.com/questions/13832720/how-to-attach-a-scrollbar-to-a-text-widget
		t = ScrolledText(f, relief=tk.RAISED, wrap=tk.WORD)
		t.insert(tk.INSERT, text)
		t.pack(fill=tk.BOTH, expand=1)
		t.bind("<KeyRelease>", self.update)
		self.nb.add(f)
		self.tabs.append(t)
		self.nb.select(self.nb.tabs()[-1])
		self.update(dirty=dirty)
	
	def update(self, key=None, dirty=True):
		if dirty and not self.dirty:
			self.dirty = True
			self.saveButton.config(text="Save&Close")
		data = [tab.get('0.0', tk.END).rstrip() for tab in self.tabs]
		self.parent.secret = self.tab_delim.join(data)
		#update tab title
		tabid = self.nb.select()
		name = data[self.nb.index(tabid)-1].rstrip().split('\n',1)[0].strip()
		self.nb.tab(tabid, text=name or "empty")

class PasswordDialog(ttk.Frame):
	def __init__(self, parent):
		ttk.Frame.__init__(self, parent)
		self.parent = parent
		
		self.parent.title("Password")
		self.style = ttk.Style()
		self.style.theme_use("default")
		self.pack(fill=tk.BOTH, expand=1)
		
		self.label = ttk.Label(self, text="Enter your Password")
		self.label.pack()
		self.entry = ttk.Entry(self, show='*')
		self.entry.bind("<KeyRelease-Return>", self.store_pass)
		self.entry.pack()
		self.entry.focus()
		button = ttk.Button(self, text="Submit", command=self.store_pass)
		button.pack()

	def store_pass(self, event=None):
		self.parent.key = self.entry.get()
		self.parent.secret = decrypt(data,self.parent.key)
		if self.parent.secret is None:
			self.label.config(text = "Wrong Password", foreground="red")
			self.entry.delete(0, tk.END)
		else:
			self.quit() #correct password
		if self.parent.key == "":
			self.quit() #user entered nothing; treat as user cancel
		
def main():
	root = tk.Tk()
	if len(argv) > 1:
		root.key = argv[1]
		root.secret = decrypt(data,root.key)
	else:
		app = PasswordDialog(root)
		root.mainloop()
		app.destroy()
	if root.secret is None:
		raise ValueError, "Wrong password" #user cancel
	root.geometry(geometry)
	root.minsize(280, 460)
	app = Window(root)
	root.mainloop()

####dammed data####

####dammed data####

if __name__ == '__main__':
	main()
