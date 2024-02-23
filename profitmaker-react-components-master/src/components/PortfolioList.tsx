import * as React from "react"
import { useState, useEffect } from 'react';

import { PortfolioListUi } from "./PortfolioListUi";

const defaultData = [
  {
    id: 30829,
    name: "Кадетский фонд",
    avatar: "",
  },
  {
    id: 41080,
    name: "Группа захвата",
    avatar: "",
  },
  {
    id: 41000,
    name: "Бюджет Deep.memo",
    avatar: "",
  },
  {
    id: 41001,
    name: "Бюджет Deep.game",
    avatar: "",
  },
  {
    id: 41002,
    name: "Бюджет Deep.social",
    avatar: "",
  },
  {
    id: 41003,
    name: "Бюджет Deep.fund",
    avatar: "",
  },
  {
    id: 41004,
    name: "Бюджет Deep.art",
    avatar: "",
  },
  {
    id: 41005,
    name: "Бюджет Deep.market",
    avatar: "",
  },
  {
    id: 41006,
    name: "Бюджет Deep.cafe",
    avatar: "",
  },
  {
    id: 41007,
    name: "Бюджет Deep.land",
    avatar: "",
  },
  {
    id: 41008,
    name: "Бюджет Deep.network",
    avatar: "",
  },
];

export const PortfolioList = () => {
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
    <PortfolioListUi search={search} setSearch={setSearch} data={data} setData={()=>{}}/>
  )
}
