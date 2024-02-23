import * as express from "express";
import {StocksController} from "./controllers/StocksController";
require("dotenv").config();

const app = express();
const port = 8080;
const pathToFront = __dirname + "/build/";
var cors = require("cors");
const corsOptions = {
    origin: "*",
    credentials: true, //access-control-allow-credentials:true
    optionSuccessStatus: 200,
};
app.use(express.static(pathToFront));
app.use(cors(corsOptions));
app.use(express.json());





app.get('/', (req: express.Request, res: express.Response) => {
    res.sendFile(pathToFront + "index.html");
    res.send('Express + TypeScript Server');
});
// app.get('/getNewsByTicker', (req: express.Request, res: express.Response) => {
//     StocksController.getNewsByTicker(req, res)
// });
app.post('/getNewsByTicker', (req: express.Request, res: express.Response) => {
    return StocksController.getNewsByTicker(req, res)
});

app.get('/getStocksList', (req: express.Request, res: express.Response) => {
    StocksController.getStocksList(req, res)
});
app.post('/getStocksList', (req: express.Request, res: express.Response) => {
    StocksController.getStocksList(req, res)
});
app.post('/getStocksList', (req: express.Request, res: express.Response) => {
    StocksController.getStocksList(req, res)
});

app.listen(port, () => {
    console.log(`⚡️[server]: Server is running at http://localhost:${port}`);
});