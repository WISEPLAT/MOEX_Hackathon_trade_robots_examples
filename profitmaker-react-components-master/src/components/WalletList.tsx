import * as React from "react"
import { useState, useEffect } from 'react';

import { WalletListUi } from "./WalletListUi";

const defaultData = [
  {
    id: 20829,
    name: "Кадетский фонд в DOGE",
    avatar: "",
    amount: 1234567.89,
    unitId: 7003,
    unitTicker: "DOGE",
    unitAvatar: "",
    unitName: "Dogecoin",
  },
  {
    id: 30080,
    name: "Группа захвата в DOGE",
    avatar: "",
    amount: 1234567.89,
    unitId: 7003,
    unitTicker: "DOGE",
    unitAvatar: "",
    unitName: "Dogecoin",
  },
  {
    id: 31000,
    name: "Бюджет Deep.memo в USD",
    avatar: "",
    amount: 1567.89,
    unitId: 7005,
    unitTicker: "USD",
    unitAvatar: "",
    unitName: "US Dollar",
  },
];

export const WalletList = () => {
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
    <WalletListUi search={search} setSearch={setSearch} data={data} />
  )
}
