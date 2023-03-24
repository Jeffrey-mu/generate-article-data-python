const fs = require('fs');

let data =fs.readdirSync('./v4')
fs.writeFile('./menu.json', JSON.stringify(data),()=>{})
