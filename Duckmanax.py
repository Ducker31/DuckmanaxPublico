import discord
from discord.ext import commands
import urllib.request
import re
import datetime
from bs4 import BeautifulSoup
import requests
import asyncio

bot = commands.Bot(command_prefix='-', description= "Este es un DuckBot")

sourceLinkAlmanax = 'http://www.krosmoz.com/es/almanax'
horaServidor = 22

def is_guild_owner():
    def InfoOwner(ctx):
        return ctx.guild is not None and ctx.guild.owner_id == ctx.author.id
    return commands.check(InfoOwner)

@bot.command()
@commands.check_any(commands.is_owner(), is_guild_owner())
async def dailyalmanax(ctx):

	anuncio = discord.Embed(title = "El Duckmanax diario a sido configurado", color=0xe5be01)
	await ctx.send(embed = anuncio)

	while 1:

		await asyncio.sleep(1)
		fechaDailyAlmanax = datetime.datetime.now()

		info = open ('info.txt','r')
		flagIOE = info.read()
		flagOE = int(flagIOE)
		print("Hora actual:", fechaDailyAlmanax.hour, ":", fechaDailyAlmanax.minute, " Token OE: ", flagOE)
		info.close()

		if fechaDailyAlmanax.hour >= horaServidor and fechaDailyAlmanax.minute >= 1 and flagOE == 0:
			info = open ('info.txt','w')
			info.write("1")
			info.close()

			print ("Procesando almanax automatico")

			source = requests.get(sourceLinkAlmanax).text
			soup = BeautifulSoup(source, 'lxml')

			mision = soup.find('div', class_='mid').p.text
			bonus = soup.find('div', class_='more').getText()
			ofrenda = soup.find('div', class_='more-infos-content').p.text
			bonus = bonus.replace(mision, "")
			bonus = bonus.replace(ofrenda, "")
			linkImagen = soup.find('div', {"class": "more-infos"}).img['src']

			fechaexacta = '{0:%d-%m-%Y}'.format(datetime.datetime.now())

			mensaje = discord.Embed(title = "`Duckmanax automatico del " + fechaexacta + "`", url=sourceLinkAlmanax, color=0xe5be01)
			mensaje.add_field(name="Mision: ", value=f"{mision}", inline=False)
			mensaje.add_field(name="Bonus: ", value=f"{bonus.strip()}", inline=False)
			mensaje.add_field(name="Ofrenda: ", value=f"{ofrenda.strip()}", inline=False)
			mensaje.set_image(url=linkImagen)
			await ctx.send(embed = mensaje)

			print("Almanax automatico enviado")

		if fechaDailyAlmanax.hour >= 0 and fechaDailyAlmanax.hour < horaServidor and flagOE == 1:
			info = open ('info.txt','w')
			info.write("0")
			info.close()
			print ("Reseteo de mensaje de almanax automatico")

@bot.command()
async def almanax(ctx):
	print("Procesando almanax")

	source = requests.get(sourceLinkAlmanax).text

	soup = BeautifulSoup(source, 'lxml')

	mision = soup.find('div', class_='mid').p.text
	bonus = soup.find('div', class_='more').getText()
	ofrenda = soup.find('div', class_='more-infos-content').p.text
	bonus = bonus.replace(mision, "")
	bonus = bonus.replace(ofrenda, "")
	linkImagen = soup.find('div', {"class": "more-infos"}).img['src']

	fechaexacta = '{0:%d-%m-%Y}'.format(datetime.datetime.now())

	mensaje = discord.Embed(title = "`Duckmanax del " + fechaexacta + "`", url=sourceLinkAlmanax, color=0xe5be01)
	mensaje.add_field(name="Mision: ", value=f"{mision}", inline=False)
	mensaje.add_field(name="Bonus: ", value=f"{bonus.strip()}", inline=False)
	mensaje.add_field(name="Ofrenda: ", value=f"{ofrenda.strip()}", inline=False)
	mensaje.set_image(url=linkImagen)
	await ctx.send(embed = mensaje)

	print("Almanax enviado")

@bot.command()
async def salmanax(ctx, busqueda: str):
	print("Procesando busqueda de almanax")
	fecha = datetime.datetime.now()
	año = fecha.year
	smes = fecha.month
	sdia = fecha.day

	for mes in range (smes,13):

		if mes > smes:
			sdia = 1
		
		for dia in range (sdia,32):

			print("Procesando Año:", año, "Mes:", mes, "Dia:", dia, "Buscando:", busqueda)

			if mes < 10:
				mes2 = "0" + str(mes)
			else:
				mes2 = mes
			if dia < 10:
				dia2 = "0" + str (dia)
			else:
				dia2 = dia

			link = "http://www.krosmoz.com/es/almanax/" + str(año) + "-" + str(mes2) + "-" + str(dia2)

			try:
				data = urllib.request.urlopen(link).read().decode('utf-8')
			except Exception as error:
				pass

			for linea in data.split("/n"):
				try:
					if re.findall(busqueda, linea, re.IGNORECASE):
						await ctx.send("Encontre esta coincidencia de " + busqueda + " : " + link)
				except Exception as error2:
					pass
	print("Busqueda de almanax finalizada")

@bot.event
async def on_message(ctx):
    if ctx.channel.name == 'almanax':
        await bot.process_commands(ctx)

@bot.event
async def on_ready():
	print("Bot listo")
	await bot.change_presence(activity=discord.Streaming(name="-almanax",url="https://www.twitch.tv/kerdrai"))

bot.run('TokenDiscord')