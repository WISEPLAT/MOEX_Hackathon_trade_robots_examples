async ({data, deep}) => {
  const UnitId = await deep.id('@suenot/unit', 'Unit');
  const WalletId = await deep.id('@suenot/wallet', 'Wallet');
  const SumId = await deep.id('@deep-foundation/payments', 'Sum');

  // const paymentValue = data?.newLink?.value?.value;
  const sumLink = (await deep.select({
    type_id: SumId,
    from_id: data?.newLink
  }))?.data?.[0];
  const paymentValue = sumLink?.value?.value || 0;

  const fromId = data?.newLink?.from_id;
  const toId = data?.newLink?.to_id;
  const fromLink = (await deep.select(fromId)).data?.[0];
  const fromValue = fromLink?.value?.value || 0;
  const fromTypeId = fromLink?.type_id;
  const toLink = (await deep.select(toId)).data?.[0];
  const toValue = toLink?.value?.value || 0;
  const toTypeId = toLink?.type_id;
  const isEmission = fromTypeId === UnitId && toTypeId === WalletId;
  const isTransfer = fromTypeId === WalletId && toTypeId === WalletId;

  if (isEmission) {
    console.log('Emission');
    const toValueResult = toValue + paymentValue;
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
    console.log({isEmission, paymentValue, toValue, toValueResult, updateToResult});
    return {isEmission, paymentValue, toValue, toValueResult, updateToResult};
  } else if (isTransfer) {
    console.log('Transfer');
    const fromValueResult = fromValue - paymentValue;
    const toValueResult = toValue + paymentValue;
    const updateFromResult = await deep.update(
      {
        link_id: fromId
      },
      {
        value: fromValueResult
      },
      {
        table: 'numbers'
      }
    )
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
    console.log({isTransfer, paymentValue, toValue, toValueResult, fromValueResult, updateFromResult, updateToResult});
    return {isTransfer, paymentValue, toValue, toValueResult, fromValueResult, updateFromResult, updateToResult};
  }
}