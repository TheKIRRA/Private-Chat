// filepath: Private_Chat/server.js
const express = require('express');
const cors = require('cors');
const http = require('http');
const { Server } = require('socket.io');
const bcrypt = require('bcrypt');
const jwt = require('jsonwebtoken');

const app = express();
const server = http.createServer(app);
const io = new Server(server);

app.use(cors());
app.use(express.json());

let chatrooms = [];
let messages = {}; // Store messages for each chatroom
const users = []; // In-memory user storage (replace with a database)

function authenticateToken(req, res, next) {
    const token = req.headers['authorization'];
    if (!token) return res.sendStatus(401);

    jwt.verify(token, 'secretkey', (err, user) => {
        if (err) return res.sendStatus(403);
        req.user = user;
        next();
    });
}

app.get('/chatrooms', authenticateToken, (req, res) => {
    res.json(chatrooms);
});

app.post('/chatrooms', (req, res) => {
    const { name } = req.body;
    if (chatrooms.length >= 3) {
        return res.status(400).json({ error: 'Maximum of 3 chatrooms allowed' });
    }
    if (chatrooms.includes(name)) {
        return res.status(400).json({ error: 'Chatroom name must be unique' });
    }
    chatrooms.push(name);
    messages[name] = []; // Initialize message storage for the chatroom
    res.status(201).json({ message: 'Chatroom created' });
});

app.delete('/chatrooms', (req, res) => {
    const { name } = req.body;
    chatrooms = chatrooms.filter(chatroom => chatroom !== name);
    delete messages[name];
    res.json({ message: 'Chatroom deleted' });
});

app.post('/register', async (req, res) => {
    const { username, password } = req.body;
    const hashedPassword = await bcrypt.hash(password, 10);
    users.push({ username, password: hashedPassword });
    res.status(201).json({ message: 'User registered' });
});

app.post('/login', async (req, res) => {
    const { username, password } = req.body;
    const user = users.find(u => u.username === username);
    if (!user || !(await bcrypt.compare(password, user.password))) {
        return res.status(401).json({ error: 'Invalid credentials' });
    }
    const token = jwt.sign({ username }, 'secretkey', { expiresIn: '1h' });
    res.json({ token });
});

// WebSocket connection
io.on('connection', (socket) => {
    console.log('A user connected');

    socket.on('joinRoom', (room) => {
        socket.join(room);
        console.log(`User joined room: ${room}`);
        socket.emit('messageHistory', messages[room] || []);
    });

    socket.on('chatMessage', ({ room, message }) => {
        const msg = { user: 'Anonymous', text: message, timestamp: new Date() };
        messages[room].push(msg);
        io.to(room).emit('newMessage', msg);
    });

    socket.on('disconnect', () => {
        console.log('A user disconnected');
    });
});

const PORT = 3000;
server.listen(PORT, () => console.log(`Server running on http://localhost:${PORT}`));