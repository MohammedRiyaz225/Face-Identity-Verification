const express = require('express');
const app = express();
const bodyParser = require('body-parser');
const multer = require('multer');
const mongoose = require('mongoose');
const path = require('path');
const mysql = require('mysql2');

// Connect to MongoDB using Mongoose
mongoose.connect('mongodb+srv://superuser:superuser123@cluster0.s3aalbl.mongodb.net/images?retryWrites=true&w=majority&appName=Cluster0', { useNewUrlParser: true, useUnifiedTopology: true });
const connection = mongoose.connection;

// Check for MongoDB connection errors
connection.on('error', console.error.bind(console, 'MongoDB connection error:'));
connection.once('open', () => {
  console.log('Connected to MongoDB');
});

// Configure multer storage
const storage = multer.memoryStorage();
const upload = multer({ storage });

// Set view engine and views directory
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

// Middleware setup
app.use(bodyParser.urlencoded({ extended: true }));
app.use(express.static(__dirname + '/web-app-main'));

// Route to render form for uploading image
app.get('/addCandidate', (req, res) => {
  res.render('addCandidate');
});

// Route to render the DnkSecurity home page
app.get('/', (req, res) => {
  const filePath = path.join(__dirname, 'web-app-main', 'index.html');
  res.sendFile(filePath);
});

const connectionM = mysql.createPool({
  connectionLimit: 10,
  host: 'localhost',
  user: 'root',
  password: '', // Leave empty if no password is set for root
  database: "ftslogin"
});

// Pool doesn't need explicit connect(), it manages connections automatically.
console.log('MySQL connection pool created');


app.get('/register', (req, res) => {

  const filePath = path.join(__dirname, '/registration_page.html');
  res.sendFile(filePath);
})
app.get('/login', (req, res) => {
  const filePath = path.join(__dirname, '/login.html');
  res.sendFile(filePath);
})


app.get('/dashboard', (req, res) => {
  const filePath = path.join(__dirname, '/Dashboard.html');
  res.sendFile(filePath);
})


app.get('/homepage', (req, res) => {
  const filePath = path.join(__dirname, '/web-app-main/index.html');
  res.sendFile(filePath);
});


//route to handle registration form
// Route to handle registration form submission


// app.post('/registrationform', (req, res) => {
//   const { username, email, password, phone_no } = req.body;

//   // Check if all fields are provided
//   if (!username || !email || !password || !phone_no) {
//     return res.status(400).send('All fields are required');
//   }

//   // Insert data into MySQL database
//   const query = 'INSERT INTO users (username, email, password, phone_no) VALUES (?, ?, ?, ?)';
//   connectionM.query(query, [username, email, password, phone_no], (error, results) => {
//     if (error) {
//       console.error('Error inserting user data into database:', error);
//       return res.status(500).send('Internal Server Error');
//     }
//     // Send back success response with a redirect to /login
//     res.redirect('/login');
//   });
// });

app.post('/registrationform', async (req, res) => {
  const { username, email, password, phone_no } = req.body;

  // Check if all fields are provided
  if (!username || !email || !password || !phone_no) {
    return res.status(400).send('All fields are required');
  }

  // Insert data into MongoDB database
  try {
    const db = mongoose.connection.db;
    const usersCollection = db.collection('users');

    // Check if user already exists
    const existingUser = await usersCollection.findOne({ username });
    if (existingUser) {
      return res.status(400).send('Username already exists');
    }

    await usersCollection.insertOne({ username, email, password, phone_no });

    // Send back success response with a redirect to the login page
    res.send(`
      <script>
        alert('Registration successful! You will be redirected to the login page.');
        window.location.href = '/login';
      </script>
    `);
  } catch (error) {
    console.error('Error inserting user data into MongoDB:', error);
    return res.status(500).send('Registration Error: ' + error.message);
  }
});

//route to handle login form

app.post('/loginform', async (req, res) => {
  const { username, password } = req.body;
  if (!username || !password) {
    return res.status(400).send('Username and password are required');
  }
  try {
    const db = mongoose.connection.db;
    const usersCollection = db.collection('users');
    const user = await usersCollection.findOne({ username, password });

    if (user) {
      // Success: Send a success response
      res.redirect('/dashboard');
    } else {
      res.redirect('/login?loginFailed=true');
    }
  } catch (error) {
    console.error('Error querying MongoDB: ' + error.stack);
    return res.status(500).send('Internal Server Error');
  }
});

// Route to handle image upload
app.post('/upload', upload.single('image'), async (req, res) => {
  // Check if file was uploaded successfully
  if (!req.file) {
    return res.status(400).send('No file uploaded.');
  }

  try {

    // wrap binary data in object

    const imagelabel = req.body.label || req.body.imageName || 'user';
    const imageData = { label: imagelabel, data: req.file.buffer };

    // Access MongoDB's native collection to insert binary data directly
    const db = mongoose.connection.db;

    // Access the 'images' collection
    const imagesCollection = db.collection('images');

    // Insert binary data into the 'images' collection
    const result = await imagesCollection.insertOne(imageData);

    console.log('Image uploaded successfully');
    // res.send('<script>alert("Image uploaded Successfully !");</script>');
    res.redirect('/dashboard');
  } catch (error) {
    console.error('Error uploading image:', error);
    res.status(500).send('Error uploading image');
  }
});

// Start the server
app.listen(3000, () => {
  console.log('Server started on port 3000');
});


//mongodb+srv://superuser:superuser123@cluster0.s3aalbl.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0
