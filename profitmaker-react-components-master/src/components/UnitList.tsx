import * as React from "react"
import { useState, useEffect } from 'react';

import { UnitListUi } from "./UnitListUi";

const defaultData = [
  {
    id: 7005,
    name: "US Dollar",
    ticker: "USD",
    avatar: "",
  },
  {
    id: 7003,
    name: "Dogecoin",
    ticker: "DOGE",
    avatar: "",
  },
  {
    id: 7004,
    name: "Bitcoin",
    ticker: "BTC",
    avatar: "",
  },
  {
    id: 7006,
    name: "Ethereum",
    ticker: "ETH",
    avatar: "",
  },
  {
    id: 7007,
    name: "Litecoin",
    ticker: "LTC",
    avatar: "",
  },
  {
    id: 7008,
    name: "Bitcoin Cash",
    ticker: "BCH",
    avatar: "",
  },
  {
    id: 7009,
    name: "Dash",
    ticker: "DASH",
    avatar: "",
  },
  {
    id: 7010,
    name: "Monero",
    ticker: "XMR",
    avatar: "",
  },
  {
    id: 7011,
    name: "Zcash",
    ticker: "ZEC",
    avatar: "",
  },
  {
    id: 7012,
    name: "Ripple",
    ticker: "XRP",
    avatar: "",
  },
  {
    id: 7013,
    name: "Stellar",
    ticker: "XLM",
    avatar: "",
  },
  {
    id: 7014,
    name: "EOS",
    ticker: "EOS",
    avatar: "",
  },
  {
    id: 7015,
    name: "Cardano",
    ticker: "ADA",
    avatar: "",
  },
  {
    id: 7016,
    name: "Tron",
    ticker: "TRX",
    avatar: "",
  },
  {
    id: 7017,
    name: "Tezos",
    ticker: "XTZ",
    avatar: "",
  },
  {
    id: 7018,
    name: "Chainlink",
    ticker: "LINK",
    avatar: "",
  },
  {
    id: 7019,
    name: "Bitcoin SV",
    ticker: "BSV",
    avatar: "",
  },
  {
    id: 7020,
    name: "Cosmos",
    ticker: "ATOM",
    avatar: "",
  },
  {
    id: 7021,
    name: "Ethereum Classic",
    ticker: "ETC",
    avatar: "",
  },
  {
    id: 7022,
    name: "NEO",
    ticker: "NEO",
    avatar: "",
  },
];

export const UnitList = () => {
  const [search, setSearch] = useState<string>('');
  const [data, setData] = useState<any[]>(defaultData);

  useEffect(() => {
    if (!search) {
      setData(defaultData);
      return;
    }
    const filteredData = defaultData.filter((item) =>
      item.name.toLowerCase().includes(search.toLowerCase()) ||
      item.id.toString().includes(search)
    );

    setData(filteredData);
  }, [search]);
  return (
    <UnitListUi search={search} setSearch={setSearch} data={data} setData={()=>{}}/>
  )
}
