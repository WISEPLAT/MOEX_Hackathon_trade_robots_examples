import * as React from "react"
import { useState, useEffect } from 'react';
import { languageToCountry } from '../languageToCountry';
import { LanguageListUi } from "./LanguageListUi";
import ISO6391 from 'iso-639-1';

const defaultData = ISO6391.getAllCodes().map(code => ({
  code,
  name: ISO6391.getName(code),
  nativeName: ISO6391.getNativeName(code),
  countryCode: languageToCountry[code],
}));
console.log({defaultData})


export const LanguageList = () => {

  const [search, setSearch] = useState<string>('');
  const [data, setData] = useState<any[]>(defaultData);

  useEffect(() => {
    if (!search) {
      setData(defaultData);
      return;
    }
    const filteredData = defaultData.filter((item) =>
      item.name.toLowerCase().toLowerCase().includes(search.toLowerCase()) ||
      item.code.toString().toLowerCase().includes(search.toLowerCase()) ||
      item.nativeName.toString().toLowerCase().includes(search.toLowerCase())
    );

    setData(filteredData);
  }, [search]);
  return (
    <LanguageListUi search={search} setSearch={setSearch} data={data} setData={setData} onSelect={(item)=>{alert(JSON.stringify(item))}} onClose={()=>{alert('close')}} />
  )
}
