

const log = console.log;
const chartProperties = {
    width: 1200,
    height: 400,
    timeScale: {
      timeVisible: true,
      secondsVisible: false,
    }
  };

var e = document.getElementById('ddlViewBy');
var hh2 = document.getElementById('hh2');
// console.log(hh2);
// hh2.innerHTML = 'New content';
const domElement = document.getElementById('custom_chart');

const chart = LightweightCharts.createChart(domElement, chartProperties);
const lineSeries = chart.addLineSeries({
    color: '#2962FF'
});




function sayThanks(){
    var instrument = e.value;
    // console.log(`http://127.0.0.1:8000/deltajur?index=` + instrument + `&bars=140`)
    hh2.innerHTML = instrument
    fetch(`http://127.0.0.1:8000/root`)
        .then(res => res.json())
        .then(json_str => JSON.parse(json_str))
        .then(data => {
            log(data['data']);
            
            ttt = data['name']

            log(ttt['idx']);

        

          // lineSeries.setData(data);
        })
        .catch(err => log(err))

}
e.addEventListener("change", function() {
  var instrument = e.value;
    // console.log(`http://127.0.0.1:8000/deltajur?index=` + instrument + `&bars=140`)
    
    const fname = fullName(instrument)
    hh2.innerHTML = fname

    chart.resize(window.innerWidth * 1, window.innerHeight * 0.7);
    fetch(`http://127.0.0.1:8000/deltajur?index=` + instrument + `&bars=180`)
        .then(res => res.json())
        .then(json_str => JSON.parse(json_str))
        .then(data => {

          lineSeries.setData(data);
          // console.log(data)
        })
        .catch(err => log(err))

    lineSeries.priceScale().applyOptions({
      autoScale: true, // disables auto scaling based on visible content
      scaleMargins: {
          top: 0.03,
          bottom: 0.03,
          left: 0.03,
      },
    });
    chart.timeScale().applyOptions({
      barSpacing: 9,
    });
});

window.addEventListener('resize', () => {
  chart.resize(window.innerWidth * 1, window.innerHeight * 0.7);
  // console.log("ksnkcn")

});


function fullName(sname) {
  lmame = ''
  switch (sname) {
    case 'AFKS':
      lmame = 'ПАО «Акционерная финансовая корпорация «Система»';
      break;
    case 'AFLT':
      lmame = 'ПАО "Аэрофлот"';
      break;
    case 'ALRS':
      lmame = 'АК "АЛРОСА" (ПАО)"';
      break;
    case 'BELU':
      lmame = 'ПАО “Белуга Групп”';
      break;
    case 'CHMF':
      lmame = 'ПАО «Северсталь»';
      break;
    case 'FEES':
      lmame = 'ПАО «Федеральная сетевая компания-Россети»';
      break;
    case 'FIVE':
      lmame = 'Икс 5 Ритейл Груп Н.В.';
      break;
    case 'FLOT':
      lmame = 'ПАО “Совкомфлот”';
      break;
    case 'GAZR':
      lmame = 'ПАО «Газпром»';
      break;
    case 'GMKN':
      lmame = 'ГМКНорНик';
      break;
    case 'GOLD':
      lmame = 'Золото';
      break;
    case 'HYDR':
      lmame = 'ПАО «РусГидро»';
      break;
    case 'IRAO':
      lmame = 'ПАО «Интер РАО ЕЭС»';
      break;
    case 'ISKJ':
      lmame = 'ПАО "ИСКЧ"';
      break;
    case 'LKOH':
      lmame = 'ПАО «НК «ЛУКОЙЛ»';
      break;
    case 'MAGN':
      lmame = 'ПАО «Магнитогорский металлургический комбинат»';
      break;
    case 'MAIL':
      lmame = 'VK';
      break;
    case 'MGNT':
      lmame = 'ПАО «Магнит»';
      break;
    case 'MOEX':
      lmame = 'ПАО Московская Биржа';
      break;
    case 'MTLR':
      lmame = 'ПАО «Мечел»';
      break;
    case 'MTSI':
      lmame = 'ПАО «МТС»';
      break;
    case 'NLMK':
      lmame = 'ПАО «НЛМК»';
      break;
    case 'NOTK':
      lmame = 'ПАО «НОВАТЭК»';
      break;
    case 'OZON':
      lmame = 'Озон Холдингс ПиЭлСи';
      break;
    case 'PHOR':
      lmame = 'ПАО "ФосАгро"';
      break;
    case 'PIKK':
      lmame = 'ПАО «ПИК СЗ»';
      break;
    case 'PLZL':
      lmame = 'ПАО «Полюс»';
      break;
    case 'POLY':
      lmame = '«Полиметалл Интернэшнл»';
      break;
    case 'POSI':
      lmame = 'ПАО "Группа Позитив"';
      break;
    case 'ROSN':
      lmame = 'Нефтяная компания "Роснефть"';
      break;
    case 'RTKM':
      lmame = 'ПАО «Ростелеком»';
      break;
    case 'RTS':
      lmame = 'Индекс РТС';
      break;
    case 'RUAL':
      lmame = 'МКПАО «ОК «РУСАЛ»';
      break;
    case 'SBPR':
      lmame = 'привилегированные акции ПАО Сбербанк';
      break;
    case 'SBRF':
      lmame = 'обыкновенные акции ПАО Сбербанк';
      break;
    case 'SGZH':
      lmame = 'ПАО “Сегежа Групп”';
      break;
    case 'SIBN':
      lmame = 'ПАО «Газпром нефть»';
      break;
    case 'SMLT':
      lmame = 'ПАО «Группа компаний «Самолет»';
      break;
    case 'SNGP':
      lmame = 'привилегированные акции ПАО «Сургутнефтегаз»';
      break;
    case 'SNGR':
      lmame = 'обыкновенные акции ПАО «Сургутнефтегаз»';
      break;
    case 'SPBE':
      lmame = 'ПАО "СПБ Биржа"';
      break; 
    case 'Si':
      lmame = 'Доллар';
      break;   
    case 'TATN':
      lmame = 'обыкновенные акции ПАО «Татнефть»';
      break; 
    case 'TCSI':
      lmame = 'ТиСиЭс Груп Холдинг ПиЭлСи';
      break; 
    case 'TRNF':
      lmame = 'привилегированные акции ПАО «Транснефть»';
      break; 
    case 'VTBR':
      lmame = 'Банк ВТБ (ПАО)';
      break;
    case 'WUSH':
      lmame = 'iВУШХолднг';
      break;
    case 'YNDF':
      lmame = 'Яндекс';
      break;


   
  }



  // console.log(`полное название ` + lmame)
  return lmame + ' (' + sname + ')'
}