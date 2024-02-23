```
const countFormRu = (number, titles) => {
  number = Math.abs(number);
  if (Number.isInteger(number)) {
    var cases = [2, 0, 1, 1, 1, 2];
    return titles[ (number%100>4 && number%100<20)? 2 : cases[(number%10<5)?number%10:5] ];
  }
  return titles[1];
}
```

const localPassangers = (number) => {
  if (language === 'ru') {
    const titles = ['пассажир', 'пассажира', 'пассажиров']
    return countFormRu(number, titles)
  } else if (language === 'en') {
    if (number > 1) {
      return 'passengers'
    } else {
      return 'passenger'
    }
  } else if (language === 'uz') {
    if (number > 1) {
      return "yo'lovchilar"
    } else {
      return "yo'lovchi"
    }
  } else {
    return formData?.passangers
  }
}