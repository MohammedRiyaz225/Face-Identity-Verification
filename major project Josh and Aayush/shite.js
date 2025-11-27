const express = require('express');
const app = express();
const bodyParser = require('body-parser');
const multer = require('multer');
const path = require('path');
const fs = require('fs');
const MongoClient = require('mongodb').MongoClient;


app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

app.use(bodyParser.urlencoded({ extended: true }));
app.engine('ejs', require('ejs').__express);

const storage = multer.memoryStorage();
const upload = multer({ storage });

app.get('/', (req, res) => {
  res.render('addCandidate');
});


app.post('/upload', upload.single('image'), (req, res) => {
  // Check if file was uploaded successfully
  if (!req.file) {
    return res.status(400).send('No file uploaded.');
  }

  // Connect to MongoDB
  MongoClient.connect('mongodb+srv://superuser:superuser123@cluster0.s3aalbl.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0', { useUnifiedTopology: true }, (err, client) => {
    if (err) {
      console.error('Failed to connect to MongoDB:', err);
      return res.status(500).send('Failed to connect to MongoDB');
    }

    // Get the database and collection
    const db = client.db('images');
    const collection = db.collection('images');

    // Insert the image into MongoDB
    collection.insertOne({ image: req.file.buffer }, (err, result) => {
      if (err) {
        console.error('Failed to insert image into MongoDB:', err);
        return res.status(500).send('Failed to insert image into MongoDB');
      }
      console.log('Image uploaded to MongoDB');
      res.redirect('/');

      // Close the MongoDB client
      client.close();
    });
  });
});


app.listen(3000, () => {
  console.log('Server started on port 3000');
});