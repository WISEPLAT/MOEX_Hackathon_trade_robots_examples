async ({data, deep}) => {
  const itemValue = data?.newLink?.value?.value;
  const fromId = data?.newLink?.from_id;
  const toId = data?.newLink?.to_id;
  const toValue = (await deep.select(toId)).data?.[0]?.value?.value || 0;
  const toValueResult = toValue + itemValue;
  const updateToResult = await deep.update(
    {
      link_id: toId
    },
    {
      value: toValueResult
    },
    {
      table: 'numbers'
    }
  )
  return {itemValue, toValue, toValueResult, updateToResult}; 
}