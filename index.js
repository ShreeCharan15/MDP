const express = require('express');
const app = express();
const http = require('http');
const server = http.createServer(app);
const { Server } = require("socket.io");
const { runModel } = require('./runModel');
const io = new Server(server);

// app.get('/', (req, res) => {
//   res.send('Hello World!')
// })

// app.post("/runModel",(req,res)=>{
//     images=req.body.paths;

    
// })

// io.on('connection', (socket) => {
//     console.log('a user connected');
    
//     socket.on('disconnect', () => {
//         console.log('user disconnected');
//     });

//     socket.on('filepaths',(files)=>{
//         console.log(files);
//         socket.emit('dd','ok');
//         socket.emit('ee','ok');
//         socket.emit('ff','ok');
//     })
// });

// server.listen(3000, () => {
//   console.log(`Example app listening on port ${3000}`)
// })

runModel()