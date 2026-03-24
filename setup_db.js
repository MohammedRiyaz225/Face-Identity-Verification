const mysql = require('mysql2');

async function testConnection() {
    const passwordsToTry = ['', 'root', 'password', '123456', 'admin'];

    for (let pwd of passwordsToTry) {
        console.log(`Trying password: "${pwd}"`);
        try {
            const connection = mysql.createConnection({
                host: 'localhost',
                user: 'root',
                password: pwd
            });

            const success = await new Promise((resolve) => {
                connection.connect((err) => {
                    if (err) {
                        console.log(`Failed to connect with password "${pwd}": ${err.message}`);
                        resolve(false);
                    } else {
                        console.log(`SUCCESS! The correct password is: "${pwd}"`);

                        // Now let's try to create the database and table
                        connection.query('CREATE DATABASE IF NOT EXISTS ftslogin', (err2) => {
                            if (err2) console.error('Error creating DB:', err2);
                            else {
                                console.log('Database ftslogin created or exists.');
                                connection.query('USE ftslogin', (err3) => {
                                    if (err3) console.error('Error USE DB:', err3);
                                    else {
                                        const createTableQuery = `
                      CREATE TABLE IF NOT EXISTS users (
                        id INT AUTO_INCREMENT PRIMARY KEY, 
                        username VARCHAR(255) NOT NULL, 
                        email VARCHAR(255) NOT NULL, 
                        password VARCHAR(255) NOT NULL, 
                        phone_no VARCHAR(20) NOT NULL
                      )
                    `;
                                        connection.query(createTableQuery, (err4) => {
                                            if (err4) console.error('Error creating table:', err4);
                                            else console.log('Table users created or exists.');
                                            connection.end();
                                        });
                                    }
                                });
                            }
                        });
                        resolve(true);
                    }
                });
            });

            if (success) {
                return pwd;
            }
        } catch (e) {
            console.error(e);
        }
    }
    console.log("None of the common passwords worked.");
    return null;
}

testConnection();
