'''
Project Name: Adventure Game
Team Members: Kelvin Bian, Amanda Lau, Kanita Sivananthan
Date: 3/22/2021
Description: Use GUI to create an dungeon themed turn based RPG adventure game 
'''

# import packages
import tkinter as tk
from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
import random
import pygame


'''Music'''
pygame.init()
#background music
music = 'Sounds/backgroundMusic.mp3'
#sound for one exchange during a battle
attackSound = pygame.mixer.Sound('Sounds/attackSound.mp3')
#sound for entering new room
door = pygame.mixer.Sound('Sounds/door.mp3')
#play background music
pygame.mixer.music.load(music)
pygame.mixer.music.play(-1)


'''Global Variables'''
#keep track of which room we are in
roomID = 1
#dictionaries for linking item/monster level with item/monster stats
roomDict = {1:1,2:2,3:5,4:10,5:15,6:25,7:40,8:178}
itemDict = {1:2,2:5,3:11,4:23,5:23,6:37,7:63,8:100}
#room names
roomNames = ["Room 1","Room 2","Room 3","Room 4","Room 5","Room 6","Room 7","Room 8"]
#track whether torches/keys/etc items have been picked up (represented by the 'Bool's) or are currently placed in the room (represented by the 'spawned's)
shieldBool = False
torchBool = False
knifeBool = False
keyBool = False
plankBool = False
candleBool = False
pplateBool = False
treasureBool = False
shieldspawned = False
torchspawned = False
knifespawned = False
keyspawned = False
plankspawned = False
candlespawned = False
pplatespawned = False
treasurespawned = False


'''Create/Set Variables'''
#create inventory for weapons and armor
inventory = []
#player and equipped weapon stats
stats = {
	"health":100,
	"attack":10,
	"sword": 0,
	"armor": 0
}


'''Classes'''
#class for equippable items (swords, armor) 
class Item:
	def __init__(self, name, itemType):
		global inventory
		self.name = name
		self.type = itemType
		self.level = itemDict[roomID]
		#item name label displayed in inventory
		self.label = None
		#item has change to have increased stats
		if(random.randint(1,10))>=8:
			self.level += int(self.level*.2)
		if(random.randint(1,10))==10:
			self.level += int(self.level*.4)
		#set item stat (health or attack) based on level and item type (sword or armor)
		if itemType == 0:
			self.stat = 10 * self.level
		elif itemType == 1:
			self.stat = 30 * self.level

	#correct the item ID
	def setID(self):
		self.id = inventory.index(self)

#class for monsters
class Monster:
	def __init__(self, x, y, name='enemy'):
		level = roomDict[roomID]
		self.name = name
		self.level = level
		#location of Monster in room
		self.x = x
		self.y = y
		#randomizes drop as armor or weapon
		self.drop = random.randint(0,1)
		#set item stat based on level
		self.health = level * 20
		self.attack = level * 5
		self.loot = None
		self.maxhealth = level * 20
		#clickable image of monster in room to initiate fight
		self.monsterImg = room_canvas.create_image(x, y, image=enemies[roomID-1])
		room_canvas.tag_bind(self.monsterImg, "<ButtonPress-1>", self.mobAttack)
		#sets item as weapon or armor
		if self.drop == 0:	
			self.loot = Item("Sword", 0)
		if self.drop == 1:
			self.loot = Item("Armor", 1)

	#called when enemy is defeated and drops its loot
	def die(self):
		if(len(inventory)>30):
			return
		inventory.append(self.loot)
		self.loot.setID()

	#calls attack to initiate a battle
	def mobAttack(self, event):
		attack(self, event)

#class for rooms' item and monster spawns
class Room:
	def __init__(self, level, monsterCount = 5):
		global shield
		global torch
		global knife
		global key
		global plank
		global candle
		global pplate
		global treasure

		global shieldspawned
		global torchspawned
		global knifespawned
		global keyspawned
		global plankspawned
		global candlespawned
		global pplatespawned
		global treasurespawned

		name = roomNames[roomID-1]
		root.title(name)
		self.level = level
		self.monsterList = []
		self.monsterCount = monsterCount

		#despawn all items in room
		if (shieldspawned):
			room_canvas.delete(shield)
			shieldspawned = False
		elif (torchspawned):
			room_canvas.delete(torch)
			torchspawned = False
		elif (knifespawned):
			room_canvas.delete(knife)
			knifespawned = False
		elif (keyspawned):
			room_canvas.delete(key)
			keyspawned = False
		elif (plankspawned):
			room_canvas.delete(plank)
			plankspawned = False
		elif (candlespawned):
			room_canvas.delete(candle)
			candlespawned = False
		elif (pplatespawned):
			room_canvas.delete(pplate)
			pplatespawned = False
		elif (treasurespawned):
			room_canvas.delete(treasure)
			treasurespawned = False
			
		#spawn the room's item
		if (roomID == 1 and not shieldBool):
			shield = room_canvas.create_image(900, 350, image=shield_img, activeimage=shieldGlow_img)
			room_canvas.tag_bind(shield, '<ButtonPress-1>', shieldPickUp)
			shieldspawned = True
		elif (roomID == 2 and not torchBool):
			torch = room_canvas.create_image(550, 150, image=torch_img, activeimage=torchGlow_img)
			room_canvas.tag_bind(torch, '<ButtonPress-1>', torchPickUp)
			torchspawned = True
		elif (roomID == 3 and not knifeBool):
			knife = room_canvas.create_image(700, 400, image=knife_img, activeimage=knifeGlow_img)
			room_canvas.tag_bind(knife, '<ButtonPress-1>', knifePickUp)
			shieldspawned = True
		elif (roomID == 4):
			monsterCount = 1
		elif(roomID == 5 and not plankBool):
			plank = room_canvas.create_image(850, 550, image=plank_img, activeimage=plankGlow_img)
			room_canvas.tag_bind(plank, '<ButtonPress-1>', plankPickUp)
			plankspawned = True
			monsterCount = 5
		elif(roomID == 6 and not candleBool):
			candle = room_canvas.create_image(950, 380, image=candle_img, activeimage=candleGlow_img)
			room_canvas.tag_bind(candle, '<ButtonPress-1>', candlePickUp)
			candlespawned = True
		#elif(roomID == 7 and not pplateBool):
		elif(roomID == 7):
			pplate = room_canvas.create_image(800, 500, image=pplate_img, activeimage=pplateGlow_img)
			room_canvas.tag_bind(pplate, '<ButtonPress-1>', pplatePickUp)
			pplatespawned = True
		elif(roomID == 8):
			monsterCount = 1
		
		#create and spawn the monster(s) in the room
		for i in range(monsterCount):
			if (roomID == 3):
				self.monsterList.append(Monster((200+i*200), 400))
			elif (roomID == 4):
				self.monsterList.append(Monster(1000, 400))
			elif (roomID == 8):
				self.monsterList.append(Monster(900, 355))
			else:
				self.monsterList.append(Monster((200+i*200), 450))


'''Functions'''
#pick up an item
def pickup(item, name):
	global shieldBool
	global torchBool
	global knifeBool
	global keyBool
	global plankBool
	global candleBool
	global pplateBool
	global treasureBool
	if(name == "shield"):
		shieldBool = True
	elif(name == "torch"):
		torchBool = True
	elif(name == "knife"):
		knifeBool = True
	elif(name == "key"):
		keyBool = True
	elif(name == "plank"):
		plankBool = True
	elif(name == "candle"):
		candleBool = True
	elif(name == "pplate"):
		pplateBool = True
	elif(name == "treasure"):
		treasureBool = True
	room_canvas.delete(item)

#calls pickup() with torch values
def torchPickUp(event):
	pickup(torch, "torch")

#calls pickup() with key values
def keyPickUp(event):
	pickup(key, "key")

#calls pickup() with shield values
def shieldPickUp(event):
	pickup(shield, "shield")

#calls pickup() with knife values
def knifePickUp(event):
	pickup(knife, "knife")

#calls pickup() with plank values
def plankPickUp(event):
	pickup(plank, "plank")

#calls pickup() with candle values
def candlePickUp(event):
	pickup(candle, "candle")

#calls pickup() with pressure plate values, multiple pressure plate interaction popups
def pplatePickUp(event):
	if(pplateBool):
		popup(room_frame, "The pressure plate is already activated.")
	elif(len(inventory)<25):
		popup(room_frame, "The pressure plate is not fully pressed.\nIf only you were heavier...")
	else:
		popup(room_frame, "You hear a *click* noise as you step on the pressure plate...")
		pickup(pplate, "pplate")

#calls pickup() with treasure values, displays end game popup message
def treasurePickUp(event):
	pickup(treasure, "treasure")
	popUp = Label(room_frame, text="CONGRATS!\nYou defeated the dragon!\nFeel free to continue roaming or leave with your treasure (exit the game).", bg='black', fg='white', justify=CENTER, bd=10)
	popUp.place(relx=0.5, rely=0.45, anchor=CENTER)
	popUp.after(5000, lambda: popUp.destroy())

#spawn enemies
def spawn(thing, x = .5, y = .5):
	thing.button.place(relx=x, rely=y)

#Move to the next room
def forward(image_number):
	global roomID
	global room_canvas
	global button_forward
	global button_back

	#check if you have required item to enter room
	if (roomID == 3):
		if (not torchBool):
			popup(room_frame, "It seems that the next room is too dark to see in...\nIt is too dangerous to proceed.")
			return
	elif (roomID == 5):
		if (not keyBool):
			popup(room_frame, "The door leading to the next room is locked...")
			return
	elif (roomID == 6):
		if (not plankBool):
			popup(room_frame, "There is no way for you to cross over the hole in the floor.\nIf only there was some kind of board...")
			return
	elif (roomID == 7):
		if (not pplateBool):
			popup(room_frame, "The pressure plate that unlocks the door is not activated.")
			return

	#increment room id by 1 
	roomID += 1
	#play the door opening sound 
	door.play()

	#clear the room canvas
	room_canvas.delete(room1)
	#place the image of the new room on the room canvas
	room_canvas.create_image(600, 300, image=room_list[image_number-1])
	#reset buttons
	button_forward.place_forget()
	button_forward=Button(button_frame, text=">>", command=lambda: forward(image_number+1))
	button_back.place_forget()
	button_back=Button(button_frame, text="<<", command=lambda: back(image_number-1))
	#prevent player from going past last room
	if image_number==8:
		button_forward=Button(button_frame, text=">>", state=DISABLED)

	button_back.place(relx=0.2, rely=0.25)
	button_forward.place(relx=0.8, rely=0.25)

	#call setup() to place everything into the room
	setup()

#Move to the previous room
def back(image_number):
	global button_forward
	global button_back
	global roomID

	#play the door opening sound 
	door.play()
	#decrese the room id by 1
	roomID -= 1

	#clear the room canvas
	room_canvas.delete(room1)
	#place the image of the new room on the room canvas
	room_canvas.create_image(600, 300, image=room_list[image_number-1])
	#reset buttons
	button_forward.place_forget()
	button_forward=Button(button_frame, text=">>", command=lambda: forward(image_number+1))
	button_back.place_forget()
	button_back= Button(button_frame, text="<<", command=lambda: back(image_number-1))
	#prevent player from going before first room
	if image_number==1:
		button_back=Button(button_frame, text="<<", state=DISABLED)

	button_back.place(relx=0.2, rely=0.25)
	button_forward.place(relx=0.8, rely=0.25)

	#call setup() to place everything into the room
	setup()

#Place all objects and enemies into the room
def setup():
	global room
	global stats

	#clear room of of previous room's monsters
	for monster in room.monsterList:
		room_canvas.delete(monster.monsterImg)
	#create new room object
	room = Room(roomDict[roomID])
	#set player stats and restore player health upon entering new room
	stats["health"] = (100 + stats["armor"])
	stats["attack"] = (10 + stats["sword"])

#opens a new window and returns it
def openNewWindow():
	newWindow = Toplevel()
	newWindow.geometry("1200x600")
    # Toplevel object which will be treated as a new window
	return newWindow

#Simulates the fight between player and enemy
#function that repeats by calling itself until fight is over. 
def fight(enemy, health_bar, newWindow, health_bar_player, event):
	fightEnd = False
	attackSound.play()

	# healthbars that update after every exchange in the fight
	if (health_bar):
		health_bar.place_forget()
	health_bar = Label(newWindow, text = str(enemy.health) + "/" + str(enemy.maxhealth), bg = 'red', width = int(30 * (enemy.health/enemy.maxhealth)), height = 2)
	health_bar.place(x=900, y=550, anchor=CENTER)
	
	if (health_bar_player):
		health_bar_player.place_forget()
	health_bar_player = Label(newWindow, text = str(stats["health"]) + "/" + str(stats["armor"]+100), bg = 'red', width = int(30 * (stats["health"]/(stats["armor"]+100))), height = 2)
	health_bar_player.place(x=300, y=550, anchor=CENTER)

	#if enemy dies, fight ends and you get a weapon/armor
	if enemy.health <= 0:
		#remove the defeated enemy from the room
		room_canvas.delete(enemy.monsterImg)
		room.monsterCount-=1
		#destroy the battle window
		newWindow.destroy()

		#open a win fight window
		WINdow = openNewWindow()
		WINdow.title("Win")
		WINdow.geometry("200x100")
		wtext = "You win!"

		#check to see if inventory has space for your weapon/armor drop
		if (len(inventory)>30):
			wtext += "\n...But you couldn't pick\nup the loot due to\na full inventory."
		else:
			wtext += "\nHave some gear!"

		#display the message
		wintext = Label(WINdow, text = wtext).place(relx=0.5, rely=0.5, anchor=CENTER)
		#destroy the win window after 2 seconds
		WINdow.after(2000, lambda: WINdow.destroy())
		enemy.die()
		fightEnd = True

		# some rooms have an item that appears after you kill an enemy in the room
		if (roomID == 4 and not keyBool):
			global key
			key = room_canvas.create_image(1000, 500, image=key_img, activeimage=keyGlow_img)
			room_canvas.tag_bind(key, '<ButtonPress-1>', keyPickUp)
			keyspawned = True
		if (roomID == 8 and not treasureBool):
			global treasure
			treasure = room_canvas.create_image(600, 450, image=treasure_img, activeimage=treasureGlow_img)
			room_canvas.tag_bind(treasure, '<ButtonPress-1>', treasurePickUp)
			treasurespawned = True
	else:
		#if you die, you are sent back one room
		if stats['health']<= 0:
			newWindow.destroy()

			#open a lose fight window
			LOSEdow = openNewWindow()
			LOSEdow.title("Lose")
			LOSEdow.geometry("200x100")
			losetext = Label(LOSEdow, text = 'You lost!\nBack to the previous room you go...').place(relx=0.5, rely=0.5, anchor=CENTER)
			#destroy the lose window after 2 seconds
			LOSEdow.after(2000, lambda: LOSEdow.destroy())
			deathscreen()
			fightEnd = True

	#you and enemy deal damage to each other
	enemy.health-=stats["attack"]
	stats["health"]-=enemy.attack

	#function calls itself if fight hasn't ended
	if (not fightEnd):
		root.after(1000, lambda: fight(enemy, health_bar, newWindow, health_bar_player, event))
		
#Rpg system
def attack(enemy, event):
	newWindow = openNewWindow()
	newWindow.title("Battle")
	
	#set background
	background = Canvas(newWindow, width=1200, height=600)
	background.pack()
	background.create_image(600, 300, image=room_list[roomID-1])

	#player image
	if (roomID == 4 or roomID == 8):
		#a small version of you for the bigger monsters
		background.create_image(300, 350, image=yousmallimg)
	else:
		background.create_image(300, 350, image=youimg)

	#enemy image
	if (roomID == 5):
		#had to add this to make it display better
		background.create_image(900, 350, image=rat_battle_img)
	else:
		background.create_image(900, 350, image=enemies[roomID-1])

	health_bar = None
	health_bar_player = None
	fight(enemy, health_bar, newWindow, health_bar_player, event)

#Opens the inventory menu after clicking the inventory button
def openinv():
	#upper frame for items in inventory
	global inv
	inv = openNewWindow()
	inv.title("Inventory")
	inv.geometry("500x600")
	inv_frame = Frame(inv)
	inv_frame.place(relwidth=1, relheight=.9)
	global canvas
	canvas = Canvas(inv_frame)
	canvas.pack(fill = BOTH, expand = 1, side = LEFT)

	#scrollbar for inventory window overflow
	scroll = ttk.Scrollbar(inv_frame, orient=VERTICAL, command=canvas.yview)
	scroll.pack(fill = Y, side = RIGHT)
	canvas.configure(yscrollcommand=scroll.set)
	canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion = canvas.bbox('all')))
	global second_frame
	second_frame = Frame(canvas)
	canvas.create_window((0,0), window=second_frame, anchor = 'nw')

	#lower frame for inventory buttons
	global inv_btn_frame
	inv_btn_frame = Frame(inv, bg='black')
	inv_btn_frame.pack(fill = BOTH, side = BOTTOM)

	#used to delete an item from inventory
	global item_delete
	item_delete = Entry(inv_btn_frame, width=5)
	item_delete.grid(row=0, column=0, padx=15)
	deleteBtn = Button(inv_btn_frame, text='Drop Item', command=delete).grid(row=0, column=2, pady=15)

	#used to equip an item from inventory
	global item_select
	item_select = Entry(inv_btn_frame, width = 5)
	item_select.grid(row=0, column = 3, padx = 15)
	selectBtn = Button(inv_btn_frame, text='Equip Item', command=equip).grid(row=0, column=4, pady=15)

	#shows current weapon/armor stat
	global infoLabel
	infoLabel = Label(inv_btn_frame, text=("Attack: " + str(stats["sword"] + 10) + "     Max health: " + str(stats["armor"] + 100)), bg='black', fg='white')
	infoLabel.grid(row=0, column=5, pady=15, padx=30)

	setInvGrid()

#displays all of your items in inventory window
def setInvGrid():
	global second_frame
	#clear the inventory window
	for widget in second_frame.winfo_children():
		widget.grid_forget()

	swordCount = 0
	armorCount = 0

	#display all weapons/armor in inventory window
	#separate column for weapons and armor
	for i in inventory:
		i.setID()
		if(i.type == 0):
			swordCount += 1
			i.typeBtn = Button(second_frame, text = i.name)
			i.typeBtn.grid(row = swordCount, column = i.type*2+1, padx = 20, pady = 10)
			i.label = Label(second_frame, text="Attack: " + str(i.stat) + ". ID: " + str(i.id))
			i.label.grid(row = swordCount, column = i.type*2+2, padx = 20, pady = 10)
		if(i.type == 1):
			armorCount += 1
			i.typeBtn = Button(second_frame, text = i.name)
			i.typeBtn.grid(row = armorCount, column = i.type*2+1, padx = 20, pady = 10)
			i.label = Label(second_frame, text="Health: " + str(i.stat) + ". ID: " + str(i.id))
			i.label.grid(row = armorCount, column = i.type*2+2, padx = 20, pady = 10)

#Deletes items from the inventory
def delete():
	#if the entry is blank, do nothing
	if (item_delete.get() == ''):
		return
	#if the entry is not a positive int, do nothing
	elif (not item_delete.get().isdigit()):
		item_delete.delete(0,END)
		return
	else:
		itemID = int(item_delete.get())
		item_delete.delete(0,END)

	#remove item from inventory
	if (inventory):
		if (itemID <= (len(inventory)-1)):
			inventory.pop(itemID)
			setInvGrid()
		else:
			popup(inv, "That item does not exist!")
	else:
		popup(inv,"You don't have any items to drop!")

#equip an item
def equip():
	#if the entry is blank, do nothing
	if (item_select.get() == ''):
		return
	#if the entry is not a positive int, do nothing
	elif (not item_select.get().isdigit()):
		item_select.delete(0,END)
		return
	elif int(item_select.get()) <= (len(inventory)-1):
		item = inventory[int(item_select.get())]
		item_select.delete(0,END)
	else:
		popup(inv, "That item does not exist!")
		item_select.delete(0,END)
		return
	
	#sets player item stat to the item stat and alerts player of the change
	if (inventory):
		if item.type == 0:
			stats["sword"] = item.stat
			popup(inv, "Equipped sword with " + str(item.stat) + " damage.")
			infoLabel = Label(inv_btn_frame, text=("Attack: " + str(stats["sword"] + 10) + "     Max health: " + str(stats["armor"] + 100)), bg='black', fg='white')
			infoLabel.grid_forget()
			infoLabel.grid(row=0, column=5, pady=15, padx=30)
		elif item.type == 1:
			stats["armor"] = item.stat
			popup(inv, "Equipped armor with " + str(item.stat) + " health.")
			infoLabel = Label(inv_btn_frame, text=("Attack: " + str(stats["sword"] + 10) + "     Max health: " + str(stats["armor"] + 100)), bg='black', fg='white')
			infoLabel.grid_forget()
			infoLabel.grid(row=0, column=5, pady=15, padx=30)
	else:
		item_select.delete(0,END)
		popup(inv, "You don't have any items to equip!")

#popups for messages
def popup(placement, message):
	popUp = Label(placement, text=message, bg='black', fg='white', justify=CENTER, bd=10)
	popUp.place(relx=0.5, rely=0.45, anchor=CENTER)
	popUp.after(3000, lambda: popUp.destroy())

#moves player back one room on player death
def deathscreen():
	back(roomID-1)


'''Build the GUI'''
root = Tk()     
root.title('Game')

#window dimensions
WIDTH = 1200
HEIGHT = 660

#Add a base canvas
base = Canvas(root, height=HEIGHT, width=WIDTH)
base.pack()

#Add an upper frame for the rooms
room_frame = Frame(base)
room_frame.place(relx=0.5, rely=0.005, relwidth=1, relheight=0.9, anchor='n')

#Make a canvas for the room image
room_canvas = Canvas(room_frame, bg="black", width=1200, height=600)
room_canvas.pack()

#import all room item images
shield_img = PhotoImage(file='Images/Shield.png')
shieldGlow_img = PhotoImage(file='Images/ShieldGlow.png')
torch_img = PhotoImage(file='Images/Torch.png')
torchGlow_img = PhotoImage(file='Images/TorchGlow.png')
knife_img = PhotoImage(file='Images/Knife.png')
knifeGlow_img = PhotoImage(file='Images/KnifeGlow.png')
key_img = PhotoImage(file='Images/Key.png')
keyGlow_img = PhotoImage(file='Images/KeyGlow.png')
plank_img = PhotoImage(file='Images/Plank.png')
plankGlow_img = PhotoImage(file='Images/PlankGlow.png')
candle_img = PhotoImage(file='Images/SusCandle.png')
candleGlow_img = PhotoImage(file='Images/SusCandle2.png')
pplate_img = PhotoImage(file='Images/Pplate.png')
pplateGlow_img = PhotoImage(file='Images/PplateGlow.png')
treasure_img = PhotoImage(file='Images/Treasure.png')
treasureGlow_img = PhotoImage(file='Images/TreasureGlow.png')

#Import the images for the backgrounds of the rooms
room1 = ImageTk.PhotoImage(Image.open('Images/Jail.png'))
room2 = ImageTk.PhotoImage(Image.open('Images/Hallway.png'))
room3 = ImageTk.PhotoImage(Image.open('Images/Armory.png'))
room4 = ImageTk.PhotoImage(Image.open('Images/WardensRoom.png'))
room5 = ImageTk.PhotoImage(Image.open('Images/Staircase.png'))
room6 = ImageTk.PhotoImage(Image.open('Images/Hole.png'))
room7 = ImageTk.PhotoImage(Image.open('Images/Office.png'))
room8 = ImageTk.PhotoImage(Image.open('Images/ThroneRoom.png'))
room_list = [room1, room2, room3, room4, room5, room6, room7, room8]

#import enemy images
bat_img = PhotoImage(file='Images/Bat.png')
slime_img = PhotoImage(file='Images/Slimes.png')
knight_img = PhotoImage(file='Images/Knight.png')
warden_img = PhotoImage(file='Images/Warden.png')
rat_img = PhotoImage(file='Images/rat.png')
rat_battle_img = PhotoImage(file='Images/ratBattle.png')
archer_img = PhotoImage(file='Images/Archer.png')
spider_img = PhotoImage(file='Images/Spider.png')
dragon_img = PhotoImage(file='Images/Dragon.png')
youimg = PhotoImage(file='Images/you.png')
yousmallimg = PhotoImage(file='Images/yousmall.png')
enemies = [bat_img, slime_img, knight_img, warden_img, rat_img, archer_img, spider_img, dragon_img]

#Add lower frame for navigation buttons
button_frame = Frame(root, bg='black')
button_frame.place(relx=0.5, rely=1, relwidth=1, relheight=0.1, anchor='s')

#Create lower frame buttons
button_back=Button(button_frame, text="<<", command=back, state=DISABLED)
button_exit=Button(button_frame, text="Exit Program", command=root.quit)
inventory_btn = Button(button_frame, text="Inventory", command=openinv)
button_forward=Button(button_frame, text=">>", command=lambda: forward(2))

#Place buttons into lower frame
button_back.place(relx=0.2, rely=0.25)
button_exit.place(relx=0.37, rely=0.25)
inventory_btn.place(relx=0.6, rely=0.25)
button_forward.place(relx=0.8, rely=0.25)

#Create the first room
room_canvas.create_image(600, 300, image=room1)
room = Room(roomDict[roomID])
setup()

root.mainloop()