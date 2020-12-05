const { MessageEmbed } = require('discord.js');

module.exports.help = {
  name: 'help',
  aliases: ['h'],
  description: 'List all available commands',
  usage: 'help [category]',
  category: 'misc',
};

module.exports.execute = ({ bot, message, args }) => {
  let str = '';

  if (args.length > 0) {
    str += `**Category: ${args[0].toUpperCase()}**\n\n`;
    bot.commands.forEach((command) => {
      if (args[0].toLowerCase() === command.help.category) {
        str += displayCommandInfo({ bot, command });
      }
    });
  } else {
    bot.commands.forEach((command) => {
      str += displayCommandInfo({ bot, command });
    });
  }

  const embed = new MessageEmbed().setTitle('Commands').setDescription(str);

  return message.channel.send(embed).catch((error) => console.error(error));
};

const displayCommandInfo = ({ bot, command }) => {
  let str = '';

  if (command.help.aliases.length !== 0) {
    str += `**${bot.config.prefix}${command.help.usage}\nAliases: ${bot.config.prefix}${command.help.aliases}**\n__Category__: *${command.help.category}*\n${command.help.description}\n\n`;
  } else {
    str += `**${bot.config.prefix}${command.help.usage}**\n__Category__: *${command.help.category}*\n${command.help.description}\n\n`;
  }

  return str;
};
