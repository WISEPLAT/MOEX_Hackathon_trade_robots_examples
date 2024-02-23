"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var express = require("express");
var StocksController_1 = require("./controllers/StocksController");
require("dotenv").config();
var app = express();
var port = 8080;
var pathToFront = __dirname + "/build/";
var cors = require("cors");
var corsOptions = {
    origin: "*",
    credentials: true, //access-control-allow-credentials:true
    optionSuccessStatus: 200,
};
app.use(express.static(pathToFront));
app.use(cors(corsOptions));
app.use(express.json());
app.get('/', function (req, res) {
    res.sendFile(pathToFront + "index.html");
    res.send('Express + TypeScript Server');
});
// app.get('/getNewsByTicker', (req: express.Request, res: express.Response) => {
//     StocksController.getNewsByTicker(req, res)
// });
app.post('/getNewsByTicker', function (req, res) {
    return StocksController_1.StocksController.getNewsByTicker(req, res);
});
app.get('/getStocksList', function (req, res) {
    StocksController_1.StocksController.getStocksList(req, res);
});
app.post('/getStocksList', function (req, res) {
    StocksController_1.StocksController.getStocksList(req, res);
});
app.post('/getStocksList', function (req, res) {
    StocksController_1.StocksController.getStocksList(req, res);
});
app.listen(port, function () {
    console.log("\u26A1\uFE0F[server]: Server is running at http://localhost:".concat(port));
});
