const { success, error, warning } = require('log-symbols');
const config = require('./config.json');
require('dotenv').config();
const Client = require('./client/Client');
const { MessageEmbed } = require('discord.js');

const bot = new Client(config);

bot.once('ready', () => {
  bot.user.setActivity({ name: `${bot.config.prefix}help`, type: "PLAYING" }).catch(error => console.error(error));
  console.log(`${success} Career Spotter bot is ready`);
});

bot.once('reconnecting', () => {
  console.log(`${success} Career Spotter bot reconnecting`);
});

bot.once('disconnect', () => {
  console.log(`${error} Career Spotter bot disconnecting`);
});

bot.on('message', async message => {
  const prefix = bot.config.prefix;
  const args = message.content.slice(prefix.length).trim().split(/ +/g);
  const cmd = args.shift().toLowerCase();

  if(message.author.bot || !message.guild) return;
  if(!message.content.startsWith(prefix)) return;

  if(cmd.length === 0) return;

  let embed = new MessageEmbed()
    .setTitle("You ran a command")
    .setDescription(`The command you ran was ${cmd}`);
  message.channel.send(embed).catch(error => console.error(error));
});

bot.login(process.env.TOKEN).catch(error => console.error(error));