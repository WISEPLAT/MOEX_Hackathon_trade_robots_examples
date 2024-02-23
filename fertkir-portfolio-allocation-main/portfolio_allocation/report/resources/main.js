function init(locale, currency, parameters) {
    const colors = [
        "#0074D9", "#FF4136", "#2ECC40", "#FF851B",
        "#7FDBFF", "#B10DC9", "#FFDC00", "#001f3f",
        "#39CCCC", "#01FF70", "#85144b", "#F012BE",
        "#3D9970", "#111111", "#AAAAAA"
    ];

    const ccyFormatter = new Intl.NumberFormat(locale, {style: 'currency', currency: currency});

    function getConfig(allocationBy, tickerToVolume) {
        const totalBalance = Object.values(tickerToVolume).reduce((a, b) => a + b, 0);

        function toLabels(tickerToVolume) {
            return Object.entries(tickerToVolume)
                .map((arr) => arr[0] + ' - ' + ccyFormatter.format(arr[1])
                    + ' (' + Math.round(arr[1] / totalBalance * 1000) / 10 + '%)');
        }

        return {
            type: 'pie',
            data: {
                labels: toLabels(tickerToVolume),
                datasets: [{
                    backgroundColor: colors,
                    borderColor: colors,
                    data: Object.values(tickerToVolume),
                }]
            },
            options: {
                plugins: {
                    title: {
                        display: true,
                        text: ['Allocation by ' + allocationBy, ccyFormatter.format(totalBalance)],
                        fullSize: true,
                        font: {
                            size: 20
                        }
                    },
                    legend: {
                        position: "right",
                        maxWidth: 300
                    },
                    tooltip: true,
                }
            }
        };
    }

    function getAllocs(aggregationKey, parameters, filterOut = {}) {
        const allocs = {};
        parameters
            .filter(p => Object.entries(filterOut)
                .flatMap(entry => Array.isArray(entry[1])
                    ? entry[1].map(value => [entry[0], value])
                    : [entry]
                )
                .map(entry => {
                    const value = p[entry[0]];
                    return value == null ||
                        (typeof value !== 'object' ? String(value) !== entry[1] : !value.hasOwnProperty(entry[1]))
                })
                .reduce((acc, cur) => acc && cur, true))
            .forEach(p => {
                let aggregationValue = p[aggregationKey];
                if (aggregationValue == null) {
                    aggregationValue = {}
                } else if (typeof aggregationValue !== 'object') {
                    aggregationValue = {[aggregationValue]: 1}
                }
                Object.entries(aggregationValue).forEach(entry => {
                    const key = entry[0];
                    const share = entry[1];
                    const existingValue = allocs[key];
                    allocs[key] = p.quantity * share + (existingValue == null ? 0 : existingValue);
                });
            });
        return Object.fromEntries(Object.entries(allocs).sort(([, a], [, b]) => b - a)); // sorting
    }

    function groupByParameter(parameters) {
        const valuesByParameter = {};
        parameters.forEach(p => {
            Object.entries(p).forEach(entry => {
                const key = entry[0];
                let values;
                if (entry[1] == null) {
                    values = []
                } else if (typeof entry[1] === 'object') {
                    values = Object.keys(entry[1]);
                } else {
                    values = [entry[1]]
                }
                const existingValue = valuesByParameter[key];
                if (existingValue == null) {
                    valuesByParameter[key] = values;
                } else {
                    valuesByParameter[key] = [...new Set([...existingValue, ...values])]
                }
            });
        });
        return valuesByParameter;
    }

    const valuesByParameter = groupByParameter(parameters);
    const allocationBySelect = document.getElementById("allocationBy")
    Object.keys(valuesByParameter).forEach(k => {
        const elem = document.createElement("option");
        elem.value = k;
        elem.innerHTML = k;
        allocationBySelect.appendChild(elem);
    });

    const settings = document.getElementById("settings");

    Object.entries(valuesByParameter).forEach(entry => {
        const parameter = entry[0];
        const values = entry[1];
        const includes = document.createElement("div");
        includes.classList.add('includes');
        includes.id = 'includes-' + parameter;
        const button = document.createElement("button");
        button.type = "button";
        button.classList.add('collapsible');
        button.innerHTML = parameter;
        includes.appendChild(button);
        const content = document.createElement("div");
        content.classList.add('content');
        includes.appendChild(content);
        values.forEach(value => {
            const checkbox = document.createElement("input");
            checkbox.setAttribute('type', 'checkbox');
            checkbox.setAttribute('checked', 'true');
            checkbox.setAttribute('parameter', parameter);
            checkbox.setAttribute('value', value);
            content.appendChild(checkbox);
            const label = document.createElement("label");
            label.innerHTML = value;
            content.appendChild(label);
            content.appendChild(document.createElement("br"));
        })
        settings.appendChild(includes);
    });
    const chart = new Chart(document.getElementById("chart"),
        getConfig(allocationBySelect.value, getAllocs(allocationBySelect.value, parameters)));

    function updateChart(filter = {}) {
        const config = getConfig(allocationBySelect.value, getAllocs(allocationBySelect.value, parameters, filter));
        chart.data = config.data;
        chart.options.plugins.title.text = config.options.plugins.title.text;
        chart.update();
    }

    allocationBySelect.addEventListener("change", updateChart);

    const filters = document.querySelectorAll('input[type=checkbox]'); // todo make selector more specific
    filters.forEach(elem => elem.addEventListener("change", () => {
        const filterOut = {};
        [].filter.call(filters, el => !el.checked).forEach(checkbox => {
            const parameter = checkbox.getAttribute('parameter');
            const value = checkbox.getAttribute('value');
            if (filterOut.hasOwnProperty(parameter)) {
                filterOut[parameter].push(value);
            } else {
                filterOut[parameter] = [value];
            }
        });
        console.log("Filter out: " + JSON.stringify(filterOut, null, 4));
        updateChart(filterOut)
    }));

    [].forEach.call(document.getElementsByClassName("collapsible"),
            elem => elem.addEventListener("click", function() {
            this.classList.toggle("active");
            const content = this.nextElementSibling;
            content.style.display = content.style.display === "block" ? "none" : "block";
        })
    );
}
