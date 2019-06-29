'use strict';

const port = 3000
const express = require('express');
const bodyParser = require('body-parser')
const cors = require('cors');

const app = express();
app.use(cors());
app.use(bodyParser.json());

app.get('/', (req, res) => res.send('Hello World!'))

app.listen(port, () => console.log(`Onboard computer REST API started in port: ${port}`))


