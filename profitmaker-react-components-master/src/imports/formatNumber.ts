export const formatNumber = ({numberToFormat, minimumFractionDigits, maximumFractionDigits}: {numberToFormat: number, minimumFractionDigits: number, maximumFractionDigits: number}) => {
  const formattedNumber = numberToFormat.toLocaleString('en-US', {
    minimumFractionDigits,
    maximumFractionDigits,
    useGrouping: true,
  });
  const formattedNumberWithSpaces = formattedNumber.replace(/,/g, ' ');
  return formattedNumberWithSpaces;
}
