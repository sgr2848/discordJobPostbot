# Career-Spotter-bot

Discord bot that updates server with new job applications and their descriptions on computer science, data science, etc.

## Installation
- Node v12 and up is required to run the bot
- Clone the repo
- Run `yarn` to install dependencies
- [Create a Discord application](https://discordjs.guide/preparations/setting-up-a-bot-application.html#creating-your-bot) and [invite the bot to your server](https://discordjs.guide/preparations/adding-your-bot-to-servers.html)
- In the project root directory, create a `.env` file and add your Discord bot token (see `.env.example` for reference)
- Run `node index.js` in the terminal and your bot should be online

## Development Setup
Prettier
```sh
yarn prettier --write .
```